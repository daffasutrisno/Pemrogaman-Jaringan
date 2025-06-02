import unittest
import socket
from io import StringIO
from unittest.mock import patch, MagicMock


def download_file(filename):
    """Download a file from the server."""
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Define address
        host = '127.0.0.1'
        port = 12345

        # Connect to server
        client_socket.connect((host, port))
        print(f"Connected to server on port {port}")
        
        # Send filename request
        client_socket.sendall(filename.encode())
        
        response = b""
        while True:
            # Receive response
            part = client_socket.recv(1024)
            if not part:
                break
            response += part
            
        print("Received from server:")
        
        # Print response
        print(response.decode())
        
    finally:
        # Close socket
        client_socket.close()
        print("Connection closed.")

def main():
    """Example usage."""
    filename = input("Enter the filename to download: ")
    download_file(filename)


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


# Unit tests
class TestDownloadFile(unittest.TestCase):
    @patch('socket.socket')
    def test_download_file_success(self, mock_socket):
        print('Testing file download success ...')
        host = '127.0.0.1'  # Localhost
        port = 12345        # Port to listen on

        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        
        # Mock the recv to simulate receiving chunks of file content
        mock_socket_instance.recv.side_effect = [b"Hello, this is the content", b" of example.txt", b""]

        # Execute
        download_file("example.txt")
        
        # Assertions
        mock_socket_instance.connect.assert_called_with((host, port))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")
        mock_socket_instance.sendall.assert_called_with(b"example.txt")
        print(f"sendall called with: {mock_socket_instance.sendall.call_args}")

    @patch('socket.socket')
    def test_download_file_non_existing(self, mock_socket):
        print('Testing file download not exist ...')
        host = '127.0.0.1'  # Localhost
        port = 12345        # Port to listen on
        
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        mock_socket_instance.recv.side_effect = [b"File not found.", b""]
        
        # Execute
        download_file("non_existent_file.txt")
        
        # Assertions
        mock_socket_instance.connect.assert_called_with((host, port))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")
        mock_socket_instance.sendall.assert_called_with(b"non_existent_file.txt")
        print(f"sendall called with: {mock_socket_instance.sendall.call_args}")
        mock_socket_instance.recv.assert_called_with(1024)
        print(f"recv called with: {mock_socket_instance.recv.call_args}")
        

if __name__ == '__main__':
    # Run unit tests
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

    # Run the client program
    # Uncomment this if you want to connect to the real server
    # main()



# Simple File Server (Client)
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