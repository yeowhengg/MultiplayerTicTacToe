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
            

    def message_handler(self, server_socket):
        while True:
            user_input = input()
            if user_input != "":
                server_socket.send(user_input.encode('utf-8'))

    def incoming_message(self, server_socket):
        while True:
            ready_sockets, _, _ = select.select(
                [server_socket], [], [], 60
            )
            if ready_sockets:
                received_board = server_socket.recv(1024)
                self.board = pickle.loads(received_board)
                self.print_board()
                
    def start_client(self):
        try:
            server_socket = socket.socket()
            # Client socket will be binded on 127.0.0.1:6969
            server_socket.connect((host, port))

        except socket.error as e:
            print(str(e))

        if server_socket.recv(2).decode('utf-8') == '-1':
            print('Sorry, server has exceeded maximum of connection. Please try again at a later time.')
            server_socket.close()

        # After establishing connection to the server, we can send messages back and forth from the server
        print(server_socket.recv(1024).decode())
        start_new_thread(self.incoming_message, (server_socket, ))
        start_new_thread(self.message_handler(server_socket, ))


client = Client()
client.start_client()
        

        


