import json
import socket
import PySimpleGUI as gui
import time
import datetime
import threading
import sys
import os


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
            else:
                break

host = socket.gethostname()  # as both code is running on same pc
port = 8080  # socket server port number

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
client_socket.connect((host, port))  # connect to the server

QUIZ = 'QUIZ Match'
gui.theme('GreenTan')  # give our window a spiffy set of colors

layout = [
    [gui.Text('please enter your name')],
    [gui.Text('Name', size=(10, 1)), gui.InputText('Name')],
    [gui.Button('Submit')]
]

window = gui.Window(QUIZ).Layout(layout)
button, values = window.Read()
window.Close()
username = values[0]
options = []

try :
    client_socket.send(username.encode()) # send username
    state = client_socket.recv(1024).decode() 
    print(state)
    if state != 'Success': #check our username in the server list or no 
        client_socket.close()
    question_No = int(client_socket.recv(1024).decode())

    for i in range(0, question_No): 

        message = client_socket.recv(1024).decode()  # receive question
        question_option = json.loads(message)
        time1 = time.time()

        # recive options 
        for j in range(0, len(question_option['options'])) :
            options.append(question_option['options'][j])

        passed_time = 0
        answered = False
        t1 = threading.Thread(target=showRemainingTime) #thread to calculate time passed 
        t1.start()

        #gui for the questions and options
        if len(question_option['options']) == 4:
            layout = [
                [gui.Text('Question')],
                [gui.Text(question_option['question'])],
                [gui.Radio(options[0], "Answer", default=True, key='1')],
                [gui.Radio(options[1], "Answer", key='2')],
                [gui.Radio(options[2], "Answer", key='3')],
                [gui.Radio(options[3], "Answer", key='4')],
                [gui.Button('Submit')]
            ]
            
            window = gui.Window(QUIZ).Layout(layout)
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
            window.Close()

        elif len(question_option['options']) == 3:
            
            layout = [
                [gui.Text('Question')],
                [gui.Text(question_option['question'])],
                [gui.Radio(options[0], "Answer", default=True, key='1')],
                [gui.Radio(options[1], "Answer", key='2')],
                [gui.Radio(options[2], "Answer", key='3')],
                [gui.Button('Submit')]
            ]

            window = gui.Window(QUIZ).Layout(layout)
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
                    
            window.Close()

        t1.join()
        if passed_time >= 45:
            print("Timeout! Your answer will not be valid for this question")
            message = "TimeOut"
            waitingLayout = [
                [gui.Text('TimeOut ! , dont answer question in 45 seconds')],
            ]
            window2 = gui.Window('TimeOut').Layout(waitingLayout)
            button, values = window2.Read(1000 * 3)
            window2.Close()

            client_socket.send(message.encode())
            t = client_socket.recv(1024).decode()
            if t != 'ok':
                client_socket.recv(1204).decode()
        else:
            client_socket.send(message.encode())  # send answer
            time2 = time.time()
            diffTime = time2 - time1
            if diffTime < 40:
                layoutChat = [[gui.Text('Your output will go here', size=(40, 1))],
                            [gui.Output(size=(110, 20), font=('Helvetica 10'))],
                            [gui.Text("Number of Message that you send : ", size=(30, 1))],
                            [gui.Text(size=(5, 1), key='-OUT-')],
                            [gui.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
                            gui.Button('SEND', button_color=(gui.YELLOWS[0], gui.BLUES[0]), bind_return_key=True),
                            ]]

                window = gui.Window('Chat window', layoutChat, font=('Helvetica', ' 13'),
                                    default_button_element_size=(8, 2), use_default_focus=False)
                
                remainingTime = 52 - diffTime
                newtime = time.time() + remainingTime

                #fuction that recv chats 
                def receive_and_print():
                    while True:
                        msg = client_socket.recv(1024).decode()
                        print(msg)

                        if msg == 'ok':
                            break
                        
                background_thread = threading.Thread(target=receive_and_print)
                background_thread.daemon = True
                background_thread.start()

                msgCount = 1
                # logic of gui updates 
                while True:
                    event, value = window.Read(timeout=1000 * int(remainingTime))
                    if time.time() > newtime - 1:
                        client_socket.send('ready'.encode())
                        break
                    if event == gui.WIN_CLOSED :
                        client_socket.send('ready'.encode())
                        break
                    elif event == 'SEND':
                        query = value['-QUERY-'].rstrip()
                        test = '{}'.format(query)
                        strr = str(username) + ': {}'.format(query)
                        time.sleep(1)
                        client_socket.send(strr.encode())
                        if str(test) == 'ready':
                            break
                    window['-OUT-'].update(msgCount)
                    msgCount += 1

                window.close()

                background_thread.join()

        score_board = json.loads(client_socket.recv(1024).decode()) # receive scoreboard

        #scoreBoard gui
        layoutScore = [
            [gui.Text('scoreBoard')],
            [gui.Text(str(score_board))]
        ]

        window1 = gui.Window(QUIZ).Layout(layoutScore)
        button, values = window1.Read(timeout=1000 * 5)
        window1.Close()

        options.clear()

    client_socket.close()  # close the connection

except :
    print("Unfortunately Connection is closed !")
