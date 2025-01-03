import socket
import hashlib
from Crypto.Cipher import ChaCha20

host = 'localhost'
secure_port = 12345
insecure_port = 12346

def receive_file(client_socket, secure=False):
    file_data = b''
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        file_data += chunk
    
    if secure:
        nonce = file_data[:8]
        ciphertext = file_data[8:]
        key = input('Enter the encryption key: ').encode()
        cipher = ChaCha20.new(key=key, nonce=nonce)
        file_data = cipher.decrypt(ciphertext)
    
    with open('downloaded_file', 'wb') as f:
        f.write(file_data)
    
    file_hash = client_socket.recv(1024).decode()
    calculated_hash = hashlib.sha256(file_data).hexdigest()
    
    if file_hash == calculated_hash:
        print('File integrity verified')
    else:
        print('File integrity check failed')

def start_client(secure):
    client_socket = socket.socket()
    
    if secure:
        client_socket.connect((host, secure_port))
    else:
        print('Warning: Connecting to insecure port')
        client_socket.connect((host, insecure_port))
    
    file_list = client_socket.recv(1024).decode().split('\n')
    print('Available files:', file_list)
    
    filename = input('Enter the name of the file to download: ')
    client_socket.sendall(filename.encode())
    
    receive_file(client_socket, secure)
    client_socket.close()

if __name__ == '__main__':
    secure = input('Connect to secure port? (yes/no): ').lower() == 'yes'
    start_client(secure)