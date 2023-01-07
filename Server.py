# Imports
import socket
from _thread import *

# Declarations
host = '127.0.0.1'
port = 6969

class Server:
    def __init__(self):
        self.MAX_CONN = 2
        self.connected_clients = []

    def incoming_message(self, server_socket: socket.socket, client_addr):
        while True:
            try:
                client_msg = server_socket.recv(2048)
                
                message = client_msg.decode('utf-8')
                print(message)

                if message.__contains__('Send all'):
                    for all_clients_sockets in self.connected_clients:
                        if all_clients_sockets != client_addr:
                            print(
                                f"{client_addr} is sending a message to everyone...")
                            all_clients_sockets.send(bytes(
                                f"Client {client_addr} has sent a message to everyone! It is: {message}", encoding='utf-8'))

                    server_socket.sendto(bytes(
                        f"You have sent the message: '{message}' to everyone!", encoding='utf-8'), client_addr)

                else:
                    print(f"Incoming message from {client_addr}: {message}")
                    server_socket.send(
                        bytes(f"Server has received your message. It is: {message}", encoding='utf-8'))
            except Exception:
                import traceback
                print(traceback.format_exc())

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

server = Server()
server.start_server(host, port)