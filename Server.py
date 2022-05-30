# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:17:06 2022

@author: YeowHeng
"""
import socket
import Game

HOST = "127.0.0.1"  # getting server's priv ipv4
PORT = 6969
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

while True:
    client_communication_socket, client_addr = server.accept()  # allow client to connect
    print(f"Connected to Client: {client_addr}")

    message = client_communication_socket.recv(1024).decode('utf-8')  # decode client's message
    print(f"Message from client is: {message}") # print client's msg

    client_communication_socket.send(f"I'm connected to you".encode('utf-8'))  # encode text to utf 8 to send

    client_communication_socket.close()  # closes socket
    print(f"Connection with {client_addr} closed")
#