# Imports
import socket
from _thread import *
from Board import *
import json
from Player import *
from random import Random

# Declarations
host = '127.0.0.1'
port = 6969

class Server:
    def __init__(self):
        self.MAX_CONN = 2
        self.connected_clients = {}
        self.players = {}
        self.board = board.get_board()

    def send_board(self):
        for all_connected_clients in self.connected_clients:
            self.connected_clients[all_connected_clients].send(bytes(json.dumps(self.board), encoding='utf-8'))

    def incoming_message(self, client_socket: socket.socket, client_address):
        while True:
            try:
                print('hello?')
                client_msg = client_socket.recv(2048)
                player_move = json.loads(client_msg.decode('utf-8'))
                row = player_move[0]
                col = player_move[1]

                player = self.players[f'{client_address}']
                print(f"Player {player.symbol} chose row: {row} col: {col}")

                board.SetPlayerInBoard(int(row), int(col), player)
                self.send_board()
            
            except Exception:
                import traceback
                print(traceback.format_exc())
                socket.close()

    # Handles new player. Assigns them with their symbols
    def client_handler(self, client_socket: socket.socket, client_address):
        print(client_address)
        client_socket.send(bytes('You are now connected to server...', encoding='utf-8'))        
        # We assign the players based on first come first serve basis
        ran = Random()
        p1 = Player(ran.choice(["X", "O"]))
        p2 = Player("")
        p2.symbol = "O" if p1.symbol == "X" else "X"
        p1.chosen = True

        self.players.update({
            f"{client_address}": p1 if p1.chosen == False else p2
        })

        player = self.players[f"{client_address}"]

        client_socket.send(bytes(f"You are player {player.symbol} :", encoding='utf-8'))
        self.send_board()

    # Accepts and assign new thread to each client
    def accept_connections(self, server_socket: socket.socket):
        client_socket, client_address = server_socket.accept()

        self.connected_clients.update({
            f"{client_address}" : client_socket 
        })

        print(f'Incoming connection accepted. Address: {client_address}')
        start_new_thread(self.client_handler, (client_socket, client_address))
        start_new_thread(self.incoming_message, (client_socket, client_address))

    def start_server(self, host, port):
        server_socket = socket.socket()

        try:
            server_socket.bind((host, port))
        except socket.error as e:
            print(str(e))

        print(f'Server is listing on port {port}...')
        
        # Accepts incoming connection
        server_socket.listen()

        while True:
            # Rejects subsequent connections if there are already 2 connected clients
            if len(self.connected_clients) >= self.MAX_CONN:
                reject_client_socket, reject_client_addr = server_socket.accept()
                reject_client_socket.send(bytes(
                    "-1", encoding='utf-8'))

                continue

            self.accept_connections(server_socket)

board = Board()
server = Server()
server.start_server(host, port)