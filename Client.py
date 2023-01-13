import socket
from _thread import *
import select
import json
from queue import Queue

host = '127.0.0.1'
port = 6969
class Client:
    def __init__(self):
        print('Waiting for connection')
        self.board = None
        self.queue = Queue()
    
    def print_board(self, board):
        self.board = json.loads(board)
        print("_______\n")
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                print("|", end='')
                print(self.board[row][col], end='')
            print("|")
            print("\n")
        print("_______")
            

    def player_move_handler(self, client_socket):
        while True:
            player_move = []
            row_input = input()

            if row_input != "":
                player_move.append(row_input)

                col_input = input()
                if col_input != "":
                    player_move.append(col_input)

                client_socket.send(bytes(json.dumps(player_move), encoding='utf-8'))
            
    def incoming_message(self, client_socket):
        while True:
            ready_sockets, _, _ = select.select(
                [client_socket], [], [], 60
            )
            if ready_sockets:
                try:
                    for sock in ready_sockets:
                        data = sock.recv(1024).decode()
                        self.queue.put(data)
                except Exception as e:
                    print(e)

    def handle_data(self):
        while True:
            data = self.queue.get()
            if data == "-2":
                continue

            print(data)
                
    def start_client(self):
        try:
            client_socket = socket.socket()
            # Client socket will be binded on 127.0.0.1:6969
            client_socket.connect((host, port))

        except socket.error as e:
            print("Error ", e)

        if client_socket.recv(2).decode('utf-8') == '-1':
            print('Sorry, client has exceeded maximum of connection. Please try again at a later time.')
            client_socket.close()

        start_new_thread(self.handle_data, ())
        start_new_thread(self.incoming_message, (client_socket, ))
        start_new_thread(self.player_move_handler(client_socket, ))


client = Client()
client.start_client()
        

        


