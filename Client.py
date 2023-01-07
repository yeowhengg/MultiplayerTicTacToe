import socket

host = '127.0.0.1'
port = 6969

client_socket = socket.socket()
print('Waiting for connection')

try:
    # Client socket will be binded on 127.0.0.1:6969
    client_socket.connect((host, port))

except socket.error as e:
    print(str(e))

if client_socket.recv(2).decode('utf-8') == '-1':
    print('Sorry, server has exceeded maximum of connection. Please try again at a later time.')
    client_socket.close()
    
else:
    # After establishing connection to the server, we can send messages back and forth from the server
    print(client_socket.recv(1024).decode('utf-8')) # Initial message
    while True:
        try:

            msg_to_send = str(input('Your message: '))
            if msg_to_send != "":
                client_socket.send(msg_to_send.encode('utf-8'))
                server_response = client_socket.recv(1024)
                print(server_response.decode('utf-8'))
                
        except Exception as e:
            print(e)

