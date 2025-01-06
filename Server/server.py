import socket
from util import *
import hashlib


# Constants
HOST = "localhost"
SECURE_PORT = 443
PORT = 1234
FILES_LIST = ["f1.txt", "f2.txt", "f3.txt"]


# Function to initialize the server socket
def initialize_server():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started at port {PORT}")
    return server_socket

# Handle secure connections
def initialize_secure_server():
    server_socket = socket.socket()
    server_socket.bind((HOST, SECURE_PORT))
    server_socket.listen()
    session, addr = server_socket.accept()
    print(f"Client connected from address: {addr} on secure port.")
    return session, addr


# Function to handle file sending
def send_file(session, file_name, secure):
    file = read_file(file_name)
    print(f"File name received: {file_name}")
    
    if secure:
        cipher_text, key, nonce = encrypt(file)
        session.send(cipher_text)
        session.send(key)
        session.send(nonce)
    else:
        send(session, file)
    
    print("File sent successfully.")


# Function to send checksum
def send_checksum(session, file):
    checksum = get_checksum(file)
    send(session, checksum)
    print("Checksum sent.")


# Main server loop
def start_server():
    server_socket = initialize_server()

    while True:
        # Accepting clients
        session, addr = server_socket.accept()
        print(f"Client connected from address: {addr}")

        # Choose connection security type
        choice = rec(session)
        secure = choice == "1"

        if secure:
            session, addr = initialize_secure_server()

        # List files
        print("Sending files list...")
        session.sendall('\n'.join(FILES_LIST).encode())

        # Receive file name and send file
        file_name = rec(session)
        send_file(session, file_name, secure)

        # Send checksum
        file = read_file(file_name)
        send_checksum(session, file)

        print("Finished :)")
        session.close()


# Start the server
if __name__ == "__main__":
    start_server()
