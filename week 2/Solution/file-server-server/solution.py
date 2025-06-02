import socket
import unittest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

files = {
    "example.txt": "Hello, this is the content of example.txt",
}

def handle_connection(conn, addr):
    print(f"Connected by {addr}")
    try:
        # receive message and decode bytes
        filename = conn.recv(1024).decode()

        # get file content from files variable in line 9
        file_content = files.get(filename, "File not found.")

        # send file content
        conn.sendall(file_content.encode())
    finally:
        # close socket
        conn.close()

def start_server():
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # define address
    host = "127.0.0.1"
    port = 12345

    # bind address to socket
    server_socket.bind((host, port))

    # listen
    server_socket.listen(1)
    print(f"Server listening on port {port}...")

    try:
        while True:
            # accept connection
            conn, addr = server_socket.accept()
            handle_connection(conn, addr)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # close server socket
        server_socket.close()

class ExitLoopException(Exception):
    pass

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

class TestFileServer(unittest.TestCase):
    @patch('socket.socket')
    def test_file_download_existing(self, mock_socket):
        print('Testing file download existing ...')
        # Setup
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b"example.txt"
        addr = ('127.0.0.1', 12345)
        
        # Test
        handle_connection(mock_conn, addr)

        mock_conn.recv.assert_called_with(1024)
        print(f"recv called with: {mock_conn.recv.call_args}")
        
        # Assertions
        mock_conn.sendall.assert_called_with(b"Hello, this is the content of example.txt")
        print(f"sendall called with: {mock_conn.sendall.call_args}")

        mock_conn.close.assert_called_once()
        print(f"close called with: {mock_conn.close.call_args}")

    @patch('socket.socket')
    def test_file_download_non_existing(self, mock_socket):
        print('Testing file download not exist ...')
        # Setup
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b"non_existing_file.txt"
        addr = ('127.0.0.1', 12345)
        
        # Test
        handle_connection(mock_conn, addr)

        mock_conn.recv.assert_called_with(1024)
        print(f"recv called with: {mock_conn.recv.call_args}")
        
        # Assertions
        mock_conn.sendall.assert_called_with(b"File not found.")
        print(f"sendall called with: {mock_conn.sendall.call_args}")

        mock_conn.close.assert_called_once()
        print(f"close called with: {mock_conn.close.call_args}")

if __name__ == '__main__':
    # uncomment this to test the server on localhost
    # start_server()

    # run unit test
    # make sure to uncomment this before submitting to domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)



#     Simple File Server (Server)
# Problem Statement:
# You are tasked with writing a simple file server and a client 
# program that can download files from the server.
# Server Requirements:
# The server should:
# - Listen on localhost (IP address 127.0.0.1) and port 12345.
# - Accept a single connection at a time.
# - When a client connects, read the requested filename from the 
# client.
# - Look up the file in an internal dictionary of files and their 
# contents.
# - Send the content of the requested file back to the client.
# - If the requested file is not found, send the message "File not 
# found." back to the client.
# - Close the connection after sending the file content or the "File 
# not found." message.
# Client Requirements:
# The client program should:
# - Take the filename as a command-line argument.
# - Connect to the server on localhost and port 12345.
# - Send the filename to the server.
# - Receive the file content (or the "File not found." message) from 
# the server.
# - Print the received content to the console.
# - Close the connection to the server.
# Input:
# Your server program should not require any input.
# Your client program should take the filename as a command-line 
# argument.
# Output of the server:
# Testing file download existing ...
# Connected by ('127.0.0.1', 12345)
# recv called with: call(1024)
# sendall called with: call(b'Hello, this is the content of 
# example.txt')
# close called with: call()
# Testing file download not exist ...
# Connected by ('127.0.0.1', 12345)
# recv called with: call(1024)
# sendall called with: call(b'File not found.')
# close called with: call()
# Output of the client:
# Testing file download not exist ...
# Connected to server on port 12345
# Received from server:
# File not found.
# Connection closed.
# connect called with: call(('127.0.0.1', 12345))
# sendall called with: call(b'non_existent_file.txt')
# recv called with: call(1024)
# Testing file download success ...
# Connected to server on port 12345
# Received from server:
# Hello, this is the content of example.txt
# Connection closed.
# connect called with: call(('127.0.0.1', 12345))
# sendall called with: call(b'example.txt')