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
        self.x_chosen = False
        self.p1_assigned = False
        self.symbol = ["X", "O"]
        self.turn = [True, False]
        self.start_game = False

    def send_board(self):
        for all_connected_clients in self.connected_clients:
            self.connected_clients[all_connected_clients].sendall(bytes(json.dumps(self.board), encoding='utf-8'))

    def handle_player_choice(self, client_socket: socket.socket, client_address):
        while self.start_game == False:
            continue
        
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

    # Handles new player. Assigns them with their symbols and also print board for them initially
    def player_handler(self, client_socket: socket.socket, client_address):
        client_socket.sendall(bytes('You are now connected to server...', encoding='utf-8'))

        # We assign the players based on first come first serve basis

        player1 = Player("")
        player2 = Player("")

        self.players.update({
            f"{client_address}": player1 if self.p1_assigned == False else player2
        })

        player = self.players[f"{client_address}"]
        ran = Random()
        player.symbol = ran.choice(self.symbol)
        player.turn = ran.choice(self.turn)
        self.turn.remove(player.turn)
        self.symbol.remove(player.symbol)
        self.p1_assigned = True

        client_socket.sendall(bytes(f"You are player {player.symbol}", encoding='utf-8'))
        while self.start_game == False:
            client_socket.sendall(bytes(f"-2", encoding='utf-8'))

            if len(self.connected_clients) == 2:
                self.start_game = True
        
        if player.turn == True:
            for client_address in self.connected_clients:
                self.connected_clients[client_address].sendall(bytes(f"It is player {player.symbol}'s turn",encoding='utf-8'))
                
    # Accepts and assign new thread to each client
    def accept_connections(self, server_socket: socket.socket):
        client_socket, client_address = server_socket.accept()

        self.connected_clients.update({
            f"{client_address}" : client_socket 
        })

        print(f'Incoming connection accepted. Address: {client_address}')
        start_new_thread(self.player_handler, (client_socket, client_address))
        start_new_thread(self.handle_player_choice, (client_socket, client_address))

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