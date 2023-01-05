import json
import socket
from _thread import *
from time import *

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


    def progress(conn, address, scoreBoard):
        count = 0
        k = 0

        while True:
            # server_socket.settimeout(30)
            # first time rcv the name
            data = conn.recv(1024).decode()
            # recv_time = time.time()
            # try :
            #     if 30 - recv_time - sendTime > 0:
                    
            print(data)

            if data == str(dataFile[k-1]['answer']):
                scoreBoard[address[1]] += 1
            conn.sendall(str.encode(json.dumps(scoreBoard)))
            print(scoreBoard)

            if k == len(data2):
                print("break")
                break

            """
            send a dict that contains question
            and options to the client.
            dump() convert dict to str.
            """
            conn.sendall(str.encode(json.dumps(data2[k])))

            # ans = conn.recv(1024).decode()
            # print(ans)

            # conn.sendall(str.encode(json.dumps(scoreBoard)))
            # if ans == str(dataFile[k-1]['answer']):
            #     scoreBoard[address[1]] += 1
            # print(scoreBoard)

            k += 1

        # print("client with port: " + str(address[1]) + " has score: " + str(score))
        conn.close()

    ThreadCount = 0

    # dict for score: key = port No. , value = score
    my_score_dict = dict()

    counter = 0
    connections = []
    addresses = []
    while True:
        conn, address = server_socket.accept()
        connections.append(conn)
        if address[1] not in my_score_dict:
            my_score_dict[address[1]] = 0
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        addresses.append(address[1])
        counter += 1
        
        # ports.append(address[1])
        if counter > 2:
            start_new_thread(progress, (connections[0], addresses[0], my_score_dict))
            start_new_thread(progress, (connections[1], addresses[1], my_score_dict))
            start_new_thread(progress, (connections[2], addresses[2], my_score_dict))

        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        print(my_score_dict)

    # server_socket.close()  # close the connection


if __name__ == '__main__':
    server_program()
