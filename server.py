import json
import socket
import time
import os
from _thread import *
from datetime import datetime
import threading

separator_token = "<SEP>" # we will use this to separate the client name & message

with open('testcase3/users.json', 'r', encoding='utf8') as file:
    usersFile = json.load(file)

clientsName = []
for i in range(0 , len(usersFile)):
    if usersFile[i]['type'] == "client" :
        clientsName.append(usersFile[i]['name'])

# get the hostname
host = socket.gethostname()

port = 8080  # initiate port no above 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance

server_socket.bind((host, port))  # bind host address and port together

server_socket.listen(3)

with open('testcase3/questions.json', 'r', encoding='utf8') as file:
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

connectionList = []
def progress(conn, addr, score_board, username):
            
        # send number of question
    conn.send(str(len(dataFile)).encode())
    
    while True:
        if len(clientsName) == 0: #until all clients are connected wait for them
            for i in range(0, len(dataFile)):
                # send question
                question = json.dumps(data2[i]).encode()
                
                conn.send(question)
                localtime1 = time.time()
                
                # receive answer
                ans = conn.recv(1024).decode()
                print(username , ":" ,  ans)

                localtime2 = time.time()
                timestamp = localtime2 - localtime1

                if ans != 'TimeOut':
                    if ans == str(dataFile[i]['answer']):
                        score_board[username] += 1

                    times = 45 - timestamp
                    newtime = time.time() + times
                    # timerThread = threading.Thread(target=timer, args=(newtime,))
                    connectionList.append(conn)
                    # this function use for chat messages
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
                                for client in connectionList:
                                    client.send(msg.encode())

                    background_thread = threading.Thread(target=input_and_send)
                    background_thread.daemon = True
                    background_thread.start()
                    background_thread.join()

                else:
                    conn.send('ok'.encode())

                time.sleep(5)
                # send score board
                conn.send(str.encode(json.dumps(score_board)))
                print(score_board)
                time.sleep(5)
                connectionList.clear()

            # bread the spin lock after quiz ended
            break
            
    conn.close()



my_score_dict = dict()
ThreadCount = 0
listOfConnections = []

while True:
    conn, address = server_socket.accept()
    username = conn.recv(1024).decode()
    
    available = False
    #check that the user wanna connect is in our list or no 
    for i in clientsName :
        if i == username :
            available = True
            clientsName.remove(i)
            list_client_name.append(username)
            listOfConnections.append(conn)  
            my_score_dict[username] = 0
            
    if available == True:
        conn.send('Success'.encode())
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(progress, (conn, address, my_score_dict, username))

        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        print(my_score_dict)
    else :
        conn.send('Failed'.encode())
        conn.close()


    