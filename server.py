# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:17:06 2022

@author: YeowHeng
"""
import socket

def host_game(self, host, port):
    
    HOST = "192.168.10.123"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        
        print(conn, addr = s.accept())
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
    
    