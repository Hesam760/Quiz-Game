import json
import socket
import pickle

def server_program():
    data2 = []
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    with open('q.json', 'r', encoding='utf8') as file:
        dataFile = json.load(file)

    def exclude_answer( i ):
        return {
            key: value for key, value in dataFile[i].items()
            if key not in 'answer'
        }
    for i in range(0, len(dataFile)):
        data2.append(exclude_answer(i))
    print(data2)

    k = 0
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        print(data)
        if k == 4:
            # if data is not received break
            break
        # send a dict that contains question and options to the client
        # dump() convert dict to str
        conn.sendall(str.encode(json.dumps(data2[k])))
        print(type(json.dumps(data2[k])))
        print(json.dumps(data2[k]))
        k += 1

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
