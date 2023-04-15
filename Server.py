# Imports
import socket, _thread
from Board import *
import json
from Player import *
from random import Random

# Declarations
host = '127.0.0.1'
port = 6969

class Server:
    def __init__(self):
        self.connected_client = {}
        self.client_socket = []
        self.sent_board = False

        self.board = board.get_board()
        self.start_server()


    def threaded_client(self, client_socket, addr, ran_symbol, ran_turn):
        player_obj = Player(ran_symbol, ran_turn)
        format_data = {addr: [client_socket, player_obj]}
        self.connected_client.update(format_data)

        while True:
            if len(self.client_socket) == 2:
                try:
                    print(self.sent_board)
                    if self.sent_board == False:
                        self.board_sender()
                        
                    else:
                        data_to_send = json.dumps([["turn", player_obj.turn], ["-1", player_obj.symbol]])
                        print(player_obj)
                        client_socket.send(data_to_send.encode())

                        self.player_data_sender()

                        # Receive data from the current client socket
                        data = client_socket.recv(1024)

                        if data:
                            row, col = data.decode("utf-8").split(",")
                            board.set_player_in_board(int(row), int(col), player_obj)
                            self.sent_board = False

                except Exception as e:
                    print("Error!", e)
        

    def board_sender(self):
        data_to_send = json.dumps(["board", self.board])
        for s in self.client_socket:
            s.sendall(data_to_send.encode())

        self.sent_board = True
    

    def player_data_sender(self):
        for addr in self.connected_client:
            client_player_object: Player = self.connected_client[addr][1]
            
            if client_player_object.turn == True:
                client_player_object.turn = False

            else:
                client_player_object.turn = True

    

    def start_server(self):
        server = "127.0.0.1"
        port = 6969
        sock = socket.socket()
        ran = Random()
        symbols = ["X", "O"]
        turn = [True, False]
        
        try:
            sock.bind((server, port))
        except socket.error as e:
            print(F"Error! {str(e)}")

        sock.listen()

        print("Started server.. Listening to incoming connections")

        while True:
            client_socket, addr = sock.accept()
            ran_symbol = ran.choice(symbols)
            symbols.pop(symbols.index(ran_symbol))

            ran_turn = ran.choice(turn)
            turn.pop(turn.index(ran_turn))

            print(f"Connected to: {addr}")
            self.client_socket.append(client_socket)
            
            _thread.start_new_thread(self.threaded_client, (client_socket, addr, ran_symbol, ran_turn))

        
board = Board()
Server()