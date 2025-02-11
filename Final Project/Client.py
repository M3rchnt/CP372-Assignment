import socket
from threading import Thread
# Provides methods for interacting with operating system
import os

class Client:
    # When creating a client, connect to the server, ask for
    # a username, and begin server communication.
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = self.socket.recv(1024).decode()
        self.locked = False

        self.talk_to_server()

    # First send over the name of the client. Then start listening
    # for messages on a separate thread. Message sending will be on 
    # the main thread.
    def talk_to_server(self):
        Thread(target = self.receive_message).start()
        self.send_message()

    # Get user input and send the message to the server
    # with the client's name prepended.
    def send_message(self):
        while True:
            if (self.locked):
                # Prevent input from occuring as Thread is currently processing an input
                continue
            client_input = input(f"{self.name}: ")
            client_message = self.name + ": " + client_input
            self.socket.send(client_message.encode())

    # Constantly listen out for messages. If the message response
    # from the server is empty, close the program.
    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            self.locked = True
            if not server_message.strip() or server_message == "Server full, rejecting connection":
                print(server_message)
                os._exit(0)
                continue
            print(f"\rMessage: {server_message}\n{self.name} ", end = "", flush=True)
            self.locked = False

if __name__ == '__main__':
    Client('127.0.0.1', 65432)