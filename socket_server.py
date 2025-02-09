import socket


def server_program():
    host = socket.gethostname() # Assuming both server and client run on the same computer, this can stay the same. If not replace the host with the desired IP to run on
    port = 65432  # initiate port 

    server_socket = socket.socket()  # get socket instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously 
    server_socket.listen(3)
    conn, address = server_socket.accept()  # accept new connection at the beginning of receiving new data
    print("Connection from: " + str(address))
    try: 
        while True:
            data = conn.recv(1024).decode() # Receive data no larger than 1024 bytes
            if not data:
                # If no data is seen, from the client, kill the connection
                print("No data received")
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())  # Send data to client
        conn.close()
    except KeyboardInterrupt:
        print("Interrupt detected, closing")
    finally:
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()