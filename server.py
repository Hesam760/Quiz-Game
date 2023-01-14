import json
import socket
import time
import os
from _thread import *
from datetime import datetime
import threading

separator_token = "<SEP>" # we will use this to separate the client name & message

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

clients = {}


def timer(time1):
    global state
    state = True
    while True:
        if time.time() > time1:
            state = False
            break
        # print(time.time() - time1)
        time.sleep(1)


def progress(conn, addr, score_board):
    print(listOfConnections)
    progress.username = conn.recv(1024).decode()
    list_client_name.append(progress.username)

    # send number of question
    conn.send(str(len(dataFile)).encode())

    while True:
        if len(list_client_name) == 3:
            for i in range(0, len(dataFile)):
                # send question

                localtime1 = time.time()
                print("t1:", localtime1)
                question = json.dumps(data2[i]).encode()

                conn.send(question)

                # receive answer
                ans = conn.recv(1024).decode()
                print(ans)

                localtime2 = time.time()
                print("t2:", localtime2)
                timestamp = localtime2 - localtime1
                print("t3:", timestamp)

                if ans != 'TimeOut':
                    if ans == str(dataFile[i]['answer']):
                        score_board[addr[1]] += 1

                    times = 45 - timestamp
                    newtime = time.time() + times
                    timerThread = threading.Thread(target=timer, args=(newtime,))
                    # timerThread.start()

                    chat = ''

                    def input_and_send():
                        while True:
                            if time.time() > newtime:
                                conn.send('ok'.encode())
                                break
                            try:
                                msg = conn.recv(1024).decode()
                                if msg == 'ready':
                                    conn.send('ok'.encode())
                                    break
                            except Exception as e:
                                print(f"[!] Error: {e}")
                                conn.close()
                            else:
                                msg = msg.replace(separator_token, ": ")
                                for client in listOfConnections:
                                    client.send(msg.encode())


                        # global chatList
                        # global stop_thread
                        # stop_thread = False
                        # chatList = []
                        # lastChat = ''
                        # while 1:
                        #     if len(chatList) == 1:
                        #         for i in chatList:
                        #             for client in listOfConnections:
                        #                 if (str(client) != str(conn)):
                        #                     client.send(i.encode())
                        #                     print("sending ", i)
                        #             chatList.clear()
                        #             break
                        #
                        #     if time.time() > newtime:
                        #         # lastChat = i
                        #         # print("lastchat:",lastChat)
                        #         break

                    background_thread = threading.Thread(target=input_and_send)
                    background_thread.daemon = True
                    # background_thread.daemon = True
                    background_thread.start()
                    background_thread.join()
                    # while True:
                    #     chat = conn.recv(1024).decode()
                    #     if (chat != ''):
                    #         print("recv chat:", chat)
                    #         chatList.append(chat)
                    #     if str(chat) == 'ready':
                    #         # stop_thread = True
                    #         break
                    #
                    # background_thread.join()
                    # conn.send('ok'.encode())
                    # time.sleep(5)
                # else :
                #     print("lastChat is : " , lastChat)
                #     if str(lastChat) != 'ready':
                #         time.sleep(2)
                #         conn.send('ok'.encode())

                else:
                    conn.send('ok'.encode())
                    # send score board
                time.sleep(5)
                conn.send(str.encode(json.dumps(score_board)))
                # conn.recv(1024).decode()
                print(score_board)
                time.sleep(5)
            # bread the spin lock after quiz ended
            break

    conn.close()


my_score_dict = dict()
ThreadCount = 0
listOfConnections = []
while True:
    conn, address = server_socket.accept()
    listOfConnections.append(conn)
    if address[1] not in my_score_dict:
        my_score_dict[address[1]] = 0
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(progress, (conn, address, my_score_dict))

    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    print(my_score_dict)