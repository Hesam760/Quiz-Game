import json
import socket
import pickle
from _thread import *

def server_program():
    data2 = []
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(3)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))

    with open('questions.json', 'r', encoding='utf8') as file:
        dataFile = json.load(file)

    def exclude_answer( i ):
        return {
            key: value for key, value in dataFile[i].items()
            if key not in 'answer'
        }
    for i in range(0, len(dataFile)):
        data2.append(exclude_answer(i))



    def progress(conn, address):
        score = 0
        k = 0
        while True:
            # first time rcv the name
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            print(data)
            if k > 0:
                if data == str(dataFile[k-1]['answer']):
                    score += 1
                    conn.sendall(str.encode(str(score)))
                else:
                    conn.sendall(str.encode(str(score)))

            if k == len(data2):
                print("len")
                # if data is not received break
                break
            # send a dict that contains question and options to the client
            # dump() convert dict to str
            conn.sendall(str.encode(json.dumps(data2[k])))
            print(type(json.dumps(data2[k])))
            print(json.dumps(data2[k]))
            k += 1
        print("client with port: " + str(address[1]) + " has score: " + str(score))
        conn.close()

    ThreadCount = 0

    # ports =[]



    while True:
        conn, address = server_socket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        # ports.append(address[1])
        start_new_thread(progress, (conn, address))
        print(conn)
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))

    # server_socket.close()  # close the connection



if __name__ == '__main__':
    server_program()
