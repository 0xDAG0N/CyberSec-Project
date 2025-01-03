import socket
import hashlib
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import os
import threading

# Define the host and ports
host = 'localhost'
secure_port = 12345
insecure_port = 12346

# List of files to send
files = ['file1.txt', 'file2.txt', 'file3.txt']

def send_file(client_socket, filename, secure=False):
    with open(filename, 'rb') as f:
        file_data = f.read()
    
    if secure:
        key = get_random_bytes(32)
        cipher = ChaCha20.new(key=key)
        ciphertext = cipher.encrypt(file_data)
        nonce = cipher.nonce
        client_socket.sendall(nonce + ciphertext)
    else:
        client_socket.sendall(file_data)
    
    # Send the hash of the file
    file_hash = hashlib.sha256(file_data).hexdigest()
    client_socket.sendall(file_hash.encode())

def handle_client(client_socket, secure=False):
    # Send the list of files
    client_socket.sendall('\n'.join(files).encode())
    
    # Receive the requested file name
    filename = client_socket.recv(1024).decode()
    
    if filename in files:
        send_file(client_socket, filename, secure)
    else:
        client_socket.sendall(b'File not found')

def handle_insecure_connections(insecure_socket):
    while True:
        print('Waiting for insecure connections...')
        client_socket, addr = insecure_socket.accept()
        print(f'Connection from {addr} on insecure port')
        handle_client(client_socket, secure=False)
        client_socket.close()

def handle_secure_connections(secure_socket):
    while True:
        print('Waiting for secure connections...')
        client_socket, addr = secure_socket.accept()
        print(f'Connection from {addr} on secure port')
        handle_client(client_socket, secure=True)
        client_socket.close()

def start_server():
    secure_socket = socket.socket()
    insecure_socket = socket.socket()
    
    secure_socket.bind((host, secure_port))
    insecure_socket.bind((host, insecure_port))
    
    secure_socket.listen(5)
    insecure_socket.listen(5)
    
    print(f'Server listening on secure port {secure_port} and insecure port {insecure_port}')
    
    threading.Thread(target=handle_insecure_connections, args=(insecure_socket,)).start()
    threading.Thread(target=handle_secure_connections, args=(secure_socket,)).start()

if __name__ == '__main__':
    start_server()
