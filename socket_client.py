import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    print(f'Client host: {host}')
    port = 65432  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while True:
        client_socket.send(message.encode())  # send message

        if (message.lower().strip() == 'bye'):
            break
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    print("Closing socket")
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()