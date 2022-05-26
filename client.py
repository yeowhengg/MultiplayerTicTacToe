# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:18:40 2022

@author: YeowHeng
"""
import socket

HOST = "192.168.10.123"  # getting server's priv ipv4
PORT = 6969

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("Connected to Server".encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))
