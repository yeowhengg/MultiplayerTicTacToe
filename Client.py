import socket
from _thread import *
import select
import json

host = '127.0.0.1'
port = 6969
class Client:
    def __init__(self):
        print('Waiting for connection')
        self.board = None
    
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
        initial_data = client_socket.recv(1024).decode()
        player, board = initial_data.split(":")
        print(player)
        self.print_board(board)

        while True:
            ready_sockets, _, _ = select.select(
                [client_socket], [], [], 60
            )
            if ready_sockets:
                try:
                    receive_board = client_socket.recv(1024).decode()
                    self.print_board(receive_board)
                except Exception as e:
                    print(e)
                
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
        
        # Prints "you are connected to server"
        print(client_socket.recv(1024).decode())

        start_new_thread(self.incoming_message, (client_socket, ))
        start_new_thread(self.player_move_handler(client_socket, ))


client = Client()
client.start_client()
        

        


