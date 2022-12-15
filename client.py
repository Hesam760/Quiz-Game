import socket
import json
import random

def client():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000 
    # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    message = str(random.randint(1,4))
    while message.lower().strip() != '0':
        data = client_socket.recv(1024).decode()  # receive response
        client_socket.settimeout(45)
        client_socket.send(message.encode())  # send message
        
        print('Received from server: ' + data)  # show in terminal
        # message =   # again take input
        break

    client_socket.close()  # close the connection
    
client()