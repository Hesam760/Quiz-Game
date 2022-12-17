import json
import socket
import PySimpleGUI as gui

def client_program():
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
        print(values)
        if values['1'] == True :
            message = '1'
        elif values['2'] == True :
            message = '2'
        elif values['3'] == True : 
            message = '3'
        elif values['4'] == True :
            message = '4'
            
        options.clear()    
        
        
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
