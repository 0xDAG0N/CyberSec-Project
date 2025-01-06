import socket
from util import *


# Constants
HOST = "localhost"
PORT = 1234
SECURE_PORT = 50000


# Function to connect to the server
def connect_to_server(host, port):
    server = socket.socket()
    server.connect((host, port))
    return server


# Function to handle connection type selection
def choose_connection_type(server):
    choice = input("Choose type of connection 1. secured 2. not secured: ")
    secure = choice == "1"
    send(server, choice)
    return secure


# Function to receive the list of files
def receive_file_list(server):
    print("Receiving files list...")
    file_list = server.recv(1024).decode().split('\n')
    print('Available files:', file_list)
    return file_list


# Function to download a file
def download_file(server, file_name, secure):
    send(server, file_name)

    if secure:
        ciphertext = server.recv(1024)
        key = server.recv(1024)
        nonce = server.recv(1024)
        print(f"Cipher text received: {ciphertext}")
        file = decrypt(ciphertext, key, nonce)
    else:
        file = rec(server)
        print(f"File data received: {file}")
    
    write_file(f"new_{file_name}", file)
    print("File downloaded.")


# Function to verify checksum
def verify_checksum(file, server):
    file_hash = get_checksum(file)
    checksum = rec(server)

    if file_hash == checksum:
        print("Checksum verified.")
    else:
        print("Checksum failed.")


# Main client loop
def start_client():
    # Connect to the server
    server = connect_to_server(HOST, PORT)

    # Choose connection type
    secure = choose_connection_type(server)

    if secure:
        server = connect_to_server(HOST, SECURE_PORT)


    # Receive file list
    file_list = receive_file_list(server)

    # Download a file
    file_name = input("Enter the name of the file you want to download: ")
    download_file(server, file_name, secure)

    # Verify checksum
    file = read_file(f"new_{file_name}")
    verify_checksum(file, server)

    # Close connection
    server.close()


# Start the client
if __name__ == "__main__":
    start_client()
