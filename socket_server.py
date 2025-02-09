import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    print(f'Server host: {host}')
    port = 65432  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(3)
    try: 
        while True:
            conn, address = server_socket.accept()  # accept new connection at the beginning of receiving new data
            print("Connection from: " + str(address))
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            print(f"Received data: {data}")
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())  # send data to the client
    except KeyboardInterrupt:
        print("Interrupt detected, closing")
    finally:
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()