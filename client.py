import json
import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" name -> ")  # take input
    i = 0
    while True:
        client_socket.send(message.encode())  # send message(include answer)
        data = json.loads(client_socket.recv(1024))  # receive response(loads() convert str to dict
        if not data:
            break
        print(f"Question {i+1}:" + data['question'])  # show in terminal
        i += 1
        print("Options:")
        for j in range(0, 4):
            print(f"{j+1}- " + data['options'][j])
        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
