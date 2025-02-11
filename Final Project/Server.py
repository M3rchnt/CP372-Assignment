import socket
from threading import Thread
import datetime

MAX_CLIENTS = 3

class Server:
    Clients = []
    Cache = []

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(MAX_CLIENTS)
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

                # Broadcast that the new client has conected
                # self.broadcast_message(client_name, client_name + " has joined the chat!")
                print(client_name + " has connected to the server. Created at: " + str(client_connection_time))

                Server.Clients.append(client)
                Server.Cache.append(client)
                Thread(target = self.handle_new_client, args = (client,)).start()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, stopping server")
        finally:
            Server.Clients.clear() 
            self.socket.close()

    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']
        while True:
            # Listen out for messages and broadcast the message to all clients. 
            client_message = client_socket.recv(1024).decode()
            # If the message is bye, remove the client from the list of clients and
            # close down the socket.
            if client_message.strip() == client_name + ": bye" or not client_message.strip():
                # self.broadcast_message(client_name, client_name + " has disconnected")
                client['client_disconnect_time'] = datetime.datetime.now()
                print(client_name + " has disconnected at: " + str(client['client_disconnect_time']))
                Server.Clients.remove(client)
                Server.Cache.remove(client)
                Server.Cache.append(client)
                client_socket.close()
                break
            elif client_message.strip() == client_name + ": status":
                self.sendStatus(client_socket)
            else:
                # Send the message to all other clients
                print("\033[1;31;40m" + client_message + "\033[0m")
                _, _, split_message = client_message.partition(" ")
                ack_message = split_message + " ACK"
                client_socket.send(ack_message.encode())
                # Thread(target = self.receive_message).start()
                # self.broadcast_message(client_name, client_message)

    # Can send the client the cache entirely or 
    # it can send each of the strings in the cache separately
    # That's alot tbh idk will figure out later.
    def sendStatus(self, client_socket): 
        status_message = "\n"
        for client in Server.Cache:
            status_message += "Client Name: " + str(client['client_name']) + "\n"
            status_message += "Client Address: " + str(client['client_socket'].getsockname()) + "\n"
            status_message += "Client Connection Time: " + str(client['client_connection_time']) + "\n"
            status_message += "Client Disconnect Time: " + str(client['client_disconnect_time']) + "\n"
        client_socket.send(status_message.encode())
        return
    # Loop through the clients and send the message down each socket.
    # Skip the socket if it's the same client.
    # def broadcast_message(self, sender_name, message): 
    #     for client in self.Clients:
    #         client_socket = client['client_socket']
    #         client_name = client['client_name']
    #         if client_name != sender_name:
    #             client_socket.send(message.encode())

if __name__ == '__main__':
    server = Server('127.0.0.1', 65432)
    server.listen()