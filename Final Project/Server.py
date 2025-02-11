import socket
from threading import Thread
import datetime
import os

MAX_CLIENTS = 3
LIST_NAME = 'repository_list'

class Server:
    Clients = []
    Cache = []

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(MAX_CLIENTS)
        if not os.path.exists(LIST_NAME): os.makedirs(LIST_NAME)
        print(f"Server is listening on {HOST}:{PORT}")
        print(f"Maximum clients allowed: {MAX_CLIENTS}")
        print("Server waiting for connection...")
        
    # Listen for connections on the main thread. When a connection
    # is received, create a new thread to handle it and add the client
    # to the list of clients.
    def listen(self):
        try:
            while True:
                client_socket, address = self.socket.accept()
                print("Attempted connection from: " + str(address))

                if (MAX_CLIENTS < len(Server.Clients) + 1):
                    client_socket.send(("Server full, rejecting connection").encode())
                    client_socket.close()
                    continue

                # The first message will be the username
                # client_name = client_socket.recv(1024).decode()
                client_name = "Client" + str(len(Server.Clients) + 1)

                # Send client name to the client
                client_socket.send(client_name.encode())

                client_connection_time = datetime.datetime.now()
                client = {'client_name': client_name, 'client_socket': client_socket, 'client_connection_time': client_connection_time, 'client_disconnect_time': None}
                clientCache = {'client_name': client_name, 'client_socket': client_socket.getsockname(), 'client_connection_time': client_connection_time, 'client_disconnect_time': None}
                print(client_name + " has connected to the server. Created at: " + str(client_connection_time))

                Server.Clients.append(client)

                Server.Cache.append(clientCache)
                Thread(target = self.handle_new_client, args = (client, clientCache)).start()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, stopping server")
        finally:
            Server.Clients.clear() 
            self.socket.close()

    def handle_new_client(self, client, clientCache):
        client_name = client['client_name']
        client_socket = client['client_socket']
        while True:
            # Listen out for messages and broadcast the message to all clients. 
            client_message = client_socket.recv(1024).decode()
            # If the message is bye, remove the client from the list of clients and
            # close down the socket.
            if client_message.strip() == client_name + ": bye" or not client_message.strip():
                client['client_disconnect_time'] = datetime.datetime.now()
                Server.Cache.remove(clientCache)
                clientCache['client_disconnect_time'] = datetime.datetime.now()
                print(client_name + " has disconnected at: " + str(client['client_disconnect_time']))
                Server.Clients.remove(client)
                Server.Cache.append(clientCache)
                client_socket.close()
                break
            # Case for if client response is status
            elif client_message.strip() == client_name + ": status":
                self.sendStatus(client_socket)
            # Case for if client response is list 
            elif client_message.strip() == client_name + ": list":
                self.sendList(client_socket)
            else:
                # Echo client message to server and print as well as send message back to client with ACK
                print("\033[1;31;40m" + client_message + "\033[0m")
                _, _, split_message = client_message.partition(" ")
                ack_message = split_message + " ACK"
                client_socket.send(ack_message.encode())

    # Handles sending the status of the cache to the client
    # Builds message starting from status_message and sends directly to client
    def sendStatus(self, client_socket): 
        status_message = "\n"
        for client in Server.Cache:
            status_message += "Client Name: " + str(client['client_name']) + "\n"
            status_message += "Client Address: " + str(client['client_socket']) + "\n"
            status_message += "Client Connection Time: " + str(client['client_connection_time']) + "\n"
            status_message += "Client Disconnect Time: " + str(client['client_disconnect_time']) + "\n"
            status_message += "--------------------\n"
        client_socket.send(status_message.encode())
    
    # Handles sending list of potential files to client from existing repository
    # Builds a list message of the files from within repository to send to client
    def sendList(self, client_socket):
        list_message = "\n"
        if (not os.listdir(LIST_NAME)): # Safety check to find if no files exist within repository, nothing to send
            list_message = "No files found in repository\n"
        else:
            list_message += "Files: "
            for file in os.listdir(LIST_NAME): # Format the files in an easier to read method
                list_message += file + " | "
        client_socket.send(list_message.encode())
    
if __name__ == '__main__':
    server = Server('127.0.0.1', 65432)
    server.listen()