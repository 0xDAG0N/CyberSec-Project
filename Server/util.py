from hashlib import sha256
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import os

# Function to receive data from the socket
def rec(soc):
    return soc.recv(1024).decode()


# Function to send data over the socket
def send(soc, data):
    if isinstance(data, bytes):
        soc.send(data)
    else:
        soc.send(data.encode())


# Function to read the content of a file
def read_file(name):
    file_path = os.path.join(os.path.dirname(__file__), name)
    with open(file_path, "r") as file:
        data = file.read()
    return data

# Function to write data to a file
def write_file(name, data):
    file_path = os.path.join(os.path.dirname(__file__), name)
    with open(file_path, "w") as file:
        file.write(data)


# Function to compute the checksum of a file (SHA-256)
def get_checksum(file):
    hash_value = sha256(file.encode()).digest()
    return hash_value.hex()


# Function to encrypt plaintext using ChaCha20
def encrypt(plaintext):
    key = get_random_bytes(32)  # Generate a random 32-byte key
    nonce = get_random_bytes(12)  # Generate a random 12-byte nonce
    cipher = ChaCha20.new(key=key, nonce=nonce)  # Initialize the cipher
    cipher_text = cipher.encrypt(plaintext.encode())  # Encrypt the plaintext
    return cipher_text, key, nonce  # Return the ciphertext, key, and nonce


# Function to decrypt ciphertext using ChaCha20
def decrypt(ciphertext, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)  # Initialize the cipher with key and nonce
    plaintext = cipher.decrypt(ciphertext)  # Decrypt the ciphertext
    return plaintext.decode()  # Return the decrypted plaintext
