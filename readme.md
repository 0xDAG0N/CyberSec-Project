# CyberSec-Project

This project demonstrates a simple client-server application with optional secure communication using ChaCha20 encryption. The server can send files to the client, and the client can verify the integrity of the received files using SHA-256 checksums.

## Project Structure
pycache/ client.py f1.txt f2.txt f3.txt server.py util.py


- `client.py`: The client-side script to connect to the server, request files, and verify checksums.
- `server.py`: The server-side script to handle client connections, send files, and provide checksums.
- `util.py`: Utility functions for file operations, encryption, and checksum calculation.
- `f1.txt`, `f2.txt`, `f3.txt`: Sample text files available for download.

## Requirements

- Python 3.x
- `pycryptodome` library for encryption

Install the required library using pip:

```sh
pip install pycryptodome

Workspace
Collecting workspace information

Sure, here is a README.md file for your project:

pycache/ client.py f1.txt f2.txt f3.txt server.py util.py

Usage
Starting the Server
Run the server script to start the server:

The server will start and listen for incoming connections on port 1234 for non-secure connections and port 443 for secure connections.

Running the Client
Run the client script to connect to the server:

The client will prompt you to choose the type of connection (secured or not secured) and then display the list of available files. Enter the name of the file you want to download.

File Download and Verification
The client will download the selected file and save it with a new_ prefix. It will also verify the checksum of the downloaded file to ensure its integrity.

Functions
Server Functions
initialize_server(): Initializes the server socket for non-secure connections.
initialize_secure_server(): Initializes the server socket for secure connections.
send_file(session, file_name, secure): Sends the requested file to the client, optionally encrypting