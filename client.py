import json
import socket
import PySimpleGUI as gui
import time
import datetime
import threading
import sys
import os
import tkinter
    
    
def showRemainingTime():
    while True:
        time.sleep(5)
        global answered
        global passed_time
        if answered:
            break
        else:
            if passed_time < 41:
                passed_time += 5
                print(str(passed_time) + " seconds passed!")
            else:
                # print("Timeout !")
                break

def timer(time1):
    global state
    state = True
    while True:
    # chat = conn.recv(1024).decode()
    # print(chat)
        if time.time() > time1: 
            state = False
            break
        # print(time.time() - time1)
        time.sleep(1)
        
            # def client_program():
            
msgList = []

host = socket.gethostname()  # as both code is running on same pc
port = 5001  # socket server port number

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
client_socket.connect((host, port))  # connect to the server


def input_and_send():
    while 1:
        message = input(str("Please enter your message: "))
        client_socket.send(message.encode())
        print("Sent")
        print("")
        
    import threading
    background_thread = threading.Thread(target=input_and_send)
    background_thread.daemon = True
    background_thread.start()

    for message in iter(lambda: client_socket.recv(1024).decode(), ''):
        print(message)
        print("")
        
QUIZ = 'QUIZ Match'
gui.theme('GreenTan') # give our window a spiffy set of colors

layout = [
    [gui.Text('please enter your name')],
    [gui.Text('Name', size=(10, 1)), gui.InputText('Name')],
    [gui.Button('Submit')]
]

window = gui.Window(QUIZ).Layout(layout)
button, values = window.Read()
window.Close()
username = values[0]
i = 0
options = []
ans = 0
count = 0

client_socket.send(username.encode())

question_No = int(client_socket.recv(1024).decode())

for i in range(0, question_No):

    message = client_socket.recv(1024).decode()  # receive question
    question_option = json.loads(message)
    time1 = time.time()

    for j in range(0, 4):
        options.append(question_option['options'][j])

    passed_time = 0
    answered = False
    t1 = threading.Thread(target=showRemainingTime)
    t1.start()

    layout = [
        [gui.Text('Question')],
        [gui.Text(question_option['question'])],
        [gui.Radio(options[0], "Answer", default=True, key='1')],
        [gui.Radio(options[1], "Answer", key='2')],
        [gui.Radio(options[2], "Answer", key='3')],
        [gui.Radio(options[3], "Answer", key='4')],
        [gui.Button('Submit')]
    ]

    # recThread = threading.Thread(target=receive)
    # recThread.start()
    
    window = gui.Window(QUIZ).Layout(layout)   
    # while True:
    button, values = window.Read(1000 * 45)
    if button == 'Submit':
        if values['1']:
            message = '1'
            answered = True
        elif values['2']:
            message = '2'
            answered = True
        elif values['3']:
            message = '3'
            answered = True
        elif values['4']:
            message = '4'
            answered = True
        # counterTime += 15
        # window['-OUT-'].update(counterTime)
        # if counterTime >= 45 :
        #     break
    window.Close()      
    
    t1.join()
    # recThread.join()
    
    if passed_time >= 45:
        print("Timeout! Your answer will not be valid for this question")
        message = "TimeOut"
        waitingLayout = [
            [gui.Text('TimeOut ! , dont answer question in 45 seconds')],
        ]
        window2 = gui.Window('TimeOut').Layout(waitingLayout)
        button , values = window2.Read(1000 * 3)
        window2.Close()
        
        client_socket.send(message.encode())
        t = client_socket.recv(1024).decode()
        print(t)
        if t != 'ok':
            client_socket.recv(1204).decode()
    else:
        client_socket.send(message.encode())    # send answer
        time2 = time.time()
        diffTime = time2 - time1
        print(40 - diffTime)
        if diffTime < 40 :
            
            layoutChat = [[gui.Text('Your output will go here', size=(40, 1))],
                    [gui.Output(size=(110, 20), font=('Helvetica 10'))],
                    [gui.Text("Number of Message that you send : ",size(30,1))],
                    [gui.Text(size = (5,1) , key ='-OUT-')],
                    [gui.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
                    gui.Button('SEND', button_color=(gui.YELLOWS[0], gui.BLUES[0]), bind_return_key=True),
                    gui.Button('EXIT', button_color=(gui.YELLOWS[0], gui.GREENS[0]))]]

            window = gui.Window('Chat window', layoutChat, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=False)
            
            remainingTime = 40 - diffTime
            newtime = time.time() + remainingTime
            
            chatList = []
            def receive_and_print():
                for message in iter(lambda: client_socket.recv(1024).decode(), ''):
                    chatList.append(message)
                    if len(chatList) == 2:
                        print(chatList[1])
                        print("")
                        chatList.clear()
                    
                    if message == 'ok' :
                        break
                    # if stop_thread == True :
                        # break
                    
            # client_socket.settimeout(45)        
            background_thread = threading.Thread(target=receive_and_print)
            # background_thread.daemon = True
            background_thread.start()
            
            
            msgCount = 1
            while True :
                event, value = window.Read(timeout = 1000 * int(remainingTime))
                if time.time() > newtime - 5:
                    client_socket.send('ready'.encode())
                    break
                if event in (gui.WIN_CLOSED, 'EXIT'):  
                    client_socket.send('ready'.encode())
                    break
                elif event == 'SEND':
                    query = value['-QUERY-'].rstrip()
                    # EXECUTE YOUR COMMAND HERE
                    test = '{}'.format(query)
                    strr = str(username) + ': {}'.format(query)
                    # print(strr, flush=True)
                    time.sleep(1)
                    client_socket.send(strr.encode())
                    if str(test) == 'ready' :
                        # stop_thread = True
                        break          
                window['-OUT-'].update(msgCount)
                msgCount += 1
            
            window.close()
            
            background_thread.join()
            
            
    # time.sleep(10)
    # time.sleep(5)           
    score_board = json.loads(client_socket.recv(1024).decode())
    
    layoutScore = [
        [gui.Text('scoreBoard')],
        [gui.Text(str(score_board))]
    ]

    window1 = gui.Window(QUIZ).Layout(layoutScore)
    button, values = window1.Read(timeout=1000 * 5)
    window1.Close()
    
    options.clear()

    
client_socket.close()  # close the connection


