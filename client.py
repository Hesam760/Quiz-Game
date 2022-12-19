import json
import socket
import PySimpleGUI as gui
import time 
import datetime
import threading

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
            else :
                print("Timeout !")
                break            
            
                
# def client_program():
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server

QUIZ = 'QUIZ Match'
layout = [
    [gui.Text('please enter your name')],
    [gui.Text('Name', size =(10,1)),gui.InputText('Name')],
    [gui.Submit()]
]

window = gui.Window(QUIZ).Layout(layout)
button , values = window.Read()
window.Close()
message = values[0]
# message = input(" name -> ")  # take input
i = 0
options = []
ans = 0
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
        options.append(data['options'][j])
    
    
    passed_time = 0
    answered = False
    t1 = threading.Thread(target = showRemainingTime)
    t1.start()
    
    layout =[
        [gui.Text('Question')],
        [gui.Text(data['question'])],
        [gui.Radio(options[0], "Answer", default=True, key='1')],
        [gui.Radio(options[1], "Answer", key='2')],
        [gui.Radio(options[2], "Answer", key='3')],
        [gui.Radio(options[3], "Answer",key='4')],
        [gui.Submit()]
    ]
    
    window = gui.Window(QUIZ).Layout(layout)
    button, values = window.Read()
    ###
    window.Close()
    print(values)
    if values['1'] == True :
        message = '1'
        answered = True
    elif values['2'] == True :
        message = '2'
        answered = True
    elif values['3'] == True : 
        message = '3'
        answered = True
    elif values['4'] == True :
        message = '4'
        answered = True
    
    t1.join()
    if passed_time >= 45 :
        # print("Timeout ! You dont answer the question")
        message = "TimeOut"
        window.Close()
    
    options.clear()    
    
    
client_socket.close()  # close the connection


# if __name__ == '__main__':
#     client_program()