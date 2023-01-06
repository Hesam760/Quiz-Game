import json
import socket
import PySimpleGUI as gui
import time
import datetime
import threading
import sys

def showRemainingTime():
    while True:
        time.sleep(5)
        global answered
        global passed_time
        if answered:
            break
        else:
            if passed_time < 45:
                passed_time += 5
                print(str(passed_time) + " seconds passed!")
            else:
                print("Timeout !")
                break

            # def client_program():


host = socket.gethostname()  # as both code is running on same pc
port = 5001  # socket server port number

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
client_socket.connect((host, port))  # connect to the server

QUIZ = 'QUIZ Match'
layout = [
    [gui.Text('please enter your name')],
    [gui.Text('Name', size=(10, 1)), gui.InputText('Name')],
    [gui.Button('Submit')]
]

window = gui.Window(QUIZ).Layout(layout)
button, values = window.Read()
window.Close()
username = values[0]
# message = input(" name -> ")  # take input
i = 0
options = []
ans = 0
count = 0

client_socket.send(username.encode())

question_No = int(client_socket.recv(1024).decode())


for i in range(0, question_No):

    message = client_socket.recv(1024).decode()  # receive question
    question_option = json.loads(message)


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
        
    window = gui.Window(QUIZ).Layout(layout)    
    window.Refresh()
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
    if button == gui.WIN_CLOSED:
        exit()
            
    window.Close()

    t1.join()
    if passed_time >= 45:
        print("Timeout! Your answer will not be valid for this question")
        message = "TimeOut"
        client_socket.send(message.encode())
    else:
        client_socket.send(message.encode())    # send answer

    score_board = json.loads(client_socket.recv(1024).decode())

    layoutScore = [
        [gui.Text('scoreBoard')],
        [gui.Text(str(score_board))]
    ]

    window.Refresh()
    window = gui.Window(QUIZ).Layout(layoutScore)
    button, values = window.Read(timeout=1000 * 5)
    window.Close()
    
    options.clear()

client_socket.close()  # close the connection