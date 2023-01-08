import socket
from _thread import *
import select
import pickle

host = '127.0.0.1'
port = 6969
class Client:
    def __init__(self):
        print('Waiting for connection')
        self.board = None
    
    def print_board(self):
        # Loop 3 times
        print("_______\n")
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                print("|", end='')
                print(self.board[row][col], end='')
            print("|")
            print("\n")
        print("_______")
            

    def message_handler(self, client_socket):
        while True:
            user_input = input()
            if user_input != "":
                client_socket.send(user_input.encode('utf-8'))

    def incoming_message(self, client_socket):
        while True:
            ready_sockets, _, _ = select.select(
                [client_socket], [], [], 60
            )
            if ready_sockets:
                received_board = client_socket.recv(1024)
                self.board = pickle.loads(received_board)
                self.print_board()
                
    def start_client(self):
        try:
            client_socket = socket.socket()
            # Client socket will be binded on 127.0.0.1:6969
            client_socket.connect((host, port))

        except socket.error as e:
            print(str(e))

        if client_socket.recv(2).decode('utf-8') == '-1':
            print('Sorry, client has exceeded maximum of connection. Please try again at a later time.')
            client_socket.close()

        # After establishing connection to the client, we can send messages back and forth from the client
        print(client_socket.recv(1024).decode())
        start_new_thread(self.incoming_message, (client_socket, ))
        start_new_thread(self.message_handler(client_socket, ))


client = Client()
client.start_client()
        

        


