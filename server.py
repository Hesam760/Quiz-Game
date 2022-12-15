import socket
import json

def server ():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    clients_scores = [0,0,0,0]
    
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    
    # read json files and put in list
    with open("q.json", "r") as file:
        fileData  = file.read()
        dataFile = json.loads(fileData)
    
    # configure how many client the server can listen simultaneously
    server_socket.listen(3)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    index = 0
    while True and dataFile[index]['question']:
        
        data = dataFile[0]['question']
        conn.send(data.encode())  # send data to the client
        for i in range(0 , 3) :
            d = dataFile[0]['options'][i]
            conn.send(d.encode()) # send
        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        datarec = conn.recv(1024).decode()
        if not datarec:
            # if data is not received break
            break
        print("from connected user: " + str(datarec))
        
        if datarec == str(dataFile[0]['answer']):
            clients_scores[0] += 1
        
        # for i in len(clients_scores):
        #     conn.send(str(clients_scores[i]).encode()) 
            
        print(clients_scores[0])
        index += 1
        break
    
    conn.close()  # close the connection
    
server()
