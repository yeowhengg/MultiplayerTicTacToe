import socket, _thread
import select
import json
from queue import Queue

host = '127.0.0.1'
port = 6969
class Client:
    def __init__(self):
        self.start_client()
        print('Waiting for connection')
    

    def print_board(self, board):
        self.board = board
        print("_______\n")
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                print("|", end='')
                print(self.board[row][col], end='')
            print("|")
            print("\n")
        print("_______")
            

    def incoming_message(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                data = json.loads(data)
                turn = False
                board = None
                
                if not data:
                    continue

                print(data)

                if "board" in data:
                    board = data[1]
                    self.print_board(board)
                    continue

                if "turn" in data[0] and "-1" in data[1]:
                    turn = data[0][1]
                    symbol = data[1][1]

                if turn == True:
                    print("It is your turn to move!")
                    row, col = self.player_input()
                    self.send_choice(row, col, client_socket)
                
                
                else:
                    print("It is other player's turn!")
                    
            except json.JSONDecodeError as e:
                print(f"Error!: {e}")
                print(data)
            
            except Exception as e:
                print(f"general exception: {e}")
                print(data)
    
    def player_input(self):
        row = str(input("Row: "))
        col = str(input("Col: "))
        return row, col
    
    
    def send_choice(self, row, col, client_socket):
        client_socket.send(bytes(str(f"{row}, {col}").encode("utf-8")))
        print("sent!")


    def start_client(self):
        try:
            # Client socket will be binded on 127.0.0.1:6969
            client_socket = socket.socket()
            client_socket.connect((host, port))
            self.incoming_message(client_socket)

        except socket.error as e:
            print("Error ", e)


Client()
        

    
    # def print_board(self, board):
    #     self.board = json.loads(board)
    #     print("_______\n")
    #     for row in range(0, len(self.board)):
    #         for col in range(0, len(self.board[row])):
    #             print("|", end='')
    #             print(self.board[row][col], end='')
    #         print("|")
    #         print("\n")
    #     print("_______")
            

    # def player_move_handler(self, client_socket):
    #     while True:
    #         player_move = []
    #         row_input = input()

    #         if row_input != "":
    #             player_move.append(row_input)

    #             col_input = input()
    #             if col_input != "":
    #                 player_move.append(col_input)

    #             client_socket.send(bytes(json.dumps(player_move), encoding='utf-8'))

        


