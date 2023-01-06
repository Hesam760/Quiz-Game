import json
import socket
import time
from _thread import *
from datetime import datetime

# get the hostname
host = socket.gethostname()

port = 5001  # initiate port no above 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance

server_socket.bind((host, port))  # bind host address and port together

server_socket.listen(3)

with open('questions.json', 'r', encoding='utf8') as file:
    dataFile = json.load(file)


def exclude_answer(i):
    return {
        key: value for key, value in dataFile[i].items()
        if key not in 'answer'
    }


data2 = []
for i in range(0, len(dataFile)):
    data2.append(exclude_answer(i))

list_client_name = []


def progress(conn, addr, score_board):

    username = conn.recv(1024).decode()
    list_client_name.append(username)

    # send number of question
    conn.send(str(len(dataFile)).encode())

    while True:
        if len(list_client_name) == 1:
            for i in range(0, len(dataFile)):
                # send question
                
                localtime1 = time.time()
                print("t1:", localtime1)
                question = json.dumps(data2[i]).encode()
                conn.send(question)
                
                # receive answer
                ans = conn.recv(1024).decode()
        
                localtime2 = time.time()
                print("t2:" , localtime2)
                timestamp = localtime2 - localtime1
                print("t3:", timestamp)
                
                if ans != 'TimeOut':
                    time.sleep(45-timestamp)

                #     #if>30 time is up.
                # if timestamp > 10:
                #     print ("Your time is up!\n")
                #     conn.close()
                if ans == str(dataFile[i]['answer']):
                    score_board[addr[1]] += 1
                    # send score board
                conn.send(str.encode(json.dumps(score_board)))
                print(score_board)

            # bread the spin lock after quiz ended
            break

    conn.close()


my_score_dict = dict()
ThreadCount = 0

while True:
    conn, address = server_socket.accept()
    if address[1] not in my_score_dict:
        my_score_dict[address[1]] = 0
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(progress, (conn, address, my_score_dict))

    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    print(my_score_dict)
