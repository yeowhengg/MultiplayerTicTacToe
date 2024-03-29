import socket
import json

host = '127.0.0.1'
port = 6969
class Client:
    def __init__(self):
        self.start_client()
        self.symbol = None
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

                if "board" in data:
                    board = data[1]
                    self.print_board(board)
                    continue
                
                if len(data) == 3 and data == "tie":
                    print("Game has tied! No moves left")
                    continue

                if "turn" in data[0] and "-1" in data[1]:
                    turn = data[0][1]
                    self.symbol = data[1][1]
                
                if len(data) == 1 and "X" or "O" in data:
                    print("You are the winner!") if self.symbol == data else print("You have lost!")
                    continue
                
                if len(data) == 3 and "-2" in data[2] and data[2] != "":
                    print(data[2][1])
                else:
                    print(f"You are: {self.symbol}")

                if turn == True:
                    print("It is your turn to move!")
                    row, col = self.player_input()
                    self.send_choice(row, col, client_socket)
                
                else:
                    print("It is other player's turn!")
                    
            except json.JSONDecodeError as e:
                print(f"Error!: {e}")
                print(len(data))
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