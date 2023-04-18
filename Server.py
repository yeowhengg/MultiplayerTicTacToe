# Imports
import socket, _thread
from Board import *
import json
from Player import *
from random import Random

# Declarations
host = '192.168.10.141'
port = 6969

class Server:
    def __init__(self):
        self.connected_client = {}
        self.client_socket = []
        self.sent_board = False
        self.count = 0
        self.col = 0

        self.board = board
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
                        
                        if self.game_logic():
                            break
                        
                        if player_obj.turn == True:
                            player_obj.turn = False
                        
                        self.send_player_data(player_obj)
                    else:

                        # Receive data from the current client socket
                        data = client_socket.recv(1024)

                        if data:
                            row, col = data.decode("utf-8").split(",")
                            
                            test = board.check_in_board(int(row), int(col), player_obj)
                            if test != True:
                                self.send_player_data(player_obj, False, test)
                                continue

                            board.set_player_in_board(int(row), int(col), player_obj)
                            self.col = int(col)
                            self.count += 1

                            self.sent_board = False
                            

                except Exception as e:
                    print("Error!", e)
        

    def board_sender(self):
        data_to_send = json.dumps(["board", self.board.get_board()])
        for s in self.client_socket:
            s.sendall(data_to_send.encode())

        self.sent_board = True

    # Sends the player's turn to everyone
    def send_player_data(self, player_obj: Player, logic = True, error_message = ""):
        for i in self.connected_client:
            if player_obj != self.connected_client[i][1] and logic:
                self.connected_client[i][1].turn = True
            elif logic == False:
                pass

            data_to_send = [["turn", self.connected_client[i][1].turn], ["-1", self.connected_client[i][1].symbol]]

            if error_message != "" and player_obj == self.connected_client[i][1]:
                data_to_send.append(["-2", error_message])

            dump_data_to_send = json.dumps(data_to_send)
            self.connected_client[i][0].sendall(dump_data_to_send.encode())
    
    def game_logic(self):
        to_return = False
        game_end = ""
        
        diagonal_win = self.board.diagonal_win()
        vertical_win = self.board.vertical_win(self.col)
        horizontal_win = self.board.horizontal_win()

        winner = ""
        
        if diagonal_win or vertical_win or horizontal_win:
            winner = "X" if "X" in (diagonal_win or vertical_win or horizontal_win) else "O"
            print(f"winner is {winner}")
            game_end = winner

            to_return = True

        if self.board.game_tie(self.count):
            game_end = "tie"
            to_return = True
        
        if game_end:
            for i in self.connected_client:
                if game_end == "tie":
                    self.connected_client[i][0].sendall(json.dumps(game_end).encode())

                else:
                    if self.connected_client[i][1].symbol == winner:
                        self.connected_client[i][0].sendall(json.dumps(game_end).encode())
                    else:
                        self.connected_client[i][0].sendall(json.dumps(game_end).encode())
        
        return to_return

    def start_server(self):
        sock = socket.socket()
        ran = Random()
        symbols = ["X", "O"]
        turn = [True, False]
        
        try:
            sock.bind((host, port))
        except socket.error as e:
            print(F"Error! {str(e)}")

        sock.listen(2)

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