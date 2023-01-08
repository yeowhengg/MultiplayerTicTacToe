# Imports
import socket
from _thread import *
from Board import *
import pickle

# Declarations
host = '127.0.0.1'
port = 6969

class Server:
    def __init__(self):
        self.MAX_CONN = 2
        self.connected_clients = []
        self.board = board.get_board()
        
    def send_board(self, server_socket: socket.socket):
        server_socket.send(pickle.dumps(self.board))

    def incoming_message(self, server_socket: socket.socket, client_addr):
        while True:
            try:
                client_msg = server_socket.recv(2048)
                message = client_msg.decode('utf-8')
                print(f"Message from client: {message}")
                self.send_board(server_socket)

            except Exception:
                import traceback
                print(traceback.format_exc())
                socket.close()

    # Handles broadcast message or single message to server
    def client_handler(self, server_socket: socket.socket, client_addr):
        server_socket.send(bytes('You are now connected to server...', encoding='utf-8'))
        start_new_thread(self.incoming_message, (server_socket, client_addr))

    # Accepts and assign new thread to each client
    def accept_connections(self, server_socket: socket.socket):
        client_socket, client_address = server_socket.accept()
        self.connected_clients.append(client_socket)
        print(f'Incoming connection accepted. Address: {client_address}')
        start_new_thread(self.client_handler, (client_socket, client_address))


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