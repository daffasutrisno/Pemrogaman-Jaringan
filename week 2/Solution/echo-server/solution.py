import socket
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

def handle_client_connection(client_socket, addr):
    """Handle a single client connection."""
    print(f"Got a connection from {addr}")

    # Receiving message
    message = client_socket.recv(1024)
    print(f"Received from client: {message.decode()}")

    
    # Sending back the message
    print(f"Sending back to client: {message.decode()}")
    client_socket.send(message)
    
    # Close the socket
    client_socket.close()

def start_server():
    """Start the server and listen for incoming connections."""
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # define address
    host = '127.0.0.1'
    port = 12345

    # bind address to socket
    server_socket.bind((host, port))
    
    # listen
    server_socket.listen(1)
    print(f"Listening on {host}:{port} ...")
    
    try:
        while True:
            # accept connection from client
            client_socket, addr = server_socket.accept()
            handle_client_connection(client_socket, addr)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # close socket
        server_socket.close()

class TestServer(unittest.TestCase):
    @patch('socket.socket')
    def test_handle_client_connection(self, mock_socket):
        """Test handling of a client connection."""
        print('Test handle_client_connection ...')
        mock_client_socket = MagicMock()
        mock_addr = ('127.0.0.1', 12345)

        mock_client_socket.recv.return_value = b'Welcome into this client-server-client sending message program!'
        
        handle_client_connection(mock_client_socket, mock_addr)
        
        mock_client_socket.recv.assert_called_with(1024)
        print(f"recv called with: {mock_client_socket.recv.call_args}")
        
        mock_client_socket.send.assert_called_with(b'Welcome into this client-server-client sending message program!')
        print(f"send called with: {mock_client_socket.send.call_args}")

        mock_client_socket.close.assert_called_once()
        print(f"close called with: {mock_client_socket.close.call_args}")

    @patch('socket.socket')
    def test_start_server(self, mock_socket):
        """Test starting of the server and listening for connections."""
        print('Test start_server ...')
        mock_server_socket = MagicMock()
        mock_client_socket = MagicMock()
        mock_addr = ('127.0.0.1', 12345)
    
        mock_socket.return_value = mock_server_socket
        mock_server_socket.accept.side_effect = [(mock_client_socket, mock_addr), KeyboardInterrupt]
        
        mock_client_socket.recv.return_value = b'Welcome into this client-server-client sending message program!'
        
        try:
            start_server()
            
        except KeyboardInterrupt:
            pass
    
        print(f"accept called with: {mock_server_socket.accept.call_args}")

        mock_server_socket.bind.assert_called_once_with(('127.0.0.1', 12345))
        print(f"bind called with: {mock_server_socket.bind.call_args}")

        mock_server_socket.listen.assert_called_once_with(1)
        print(f"listen called with: {mock_server_socket.listen.call_args}")

class NullWriter(StringIO):
    def write(self, txt):
        pass

if __name__ == '__main__':
    # Run unittest with a custom runner that suppresses output
    # Make sure to uncomment this before uploading the code to domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

    # Uncomment this if you want to run the server program, not running the unit test
    # start_server()




# cho Server (Server)
# Description
# In this programming challenge, you are tasked with implementing a 
# basic "echo server". An echo server simply sends back the same 
# message it receives from a client. This requires setting up both a 
# server and a client. The client sends a message to the server, the 
# server receives this message, and then the server sends the same 
# message back to the client. The client then verifies the received 
# message matches the one sent.
# Input
# No direct input is provided through standard input as this challenge 
# involves network communication. The client will programmatically 
# send a predefined message to the server using TCP/IP sockets. The 
# server is expected to listen on localhost (127.0.0.1) at a 
# predefined port (e.g., 12345).
# Output
# The client should print to the console the message received from the 
# server. This output should match the original message sent by the 
# client, demonstrating a successful echo.
# For the sake of example, if the client sends the message "Hello, 
# Echo Server!", the expected output is: Received from server: Hello, 
# Echo Server!
# Method
# Your solution should include both a server and a client program as 
# follows:
# - Server Program: The server should bind to the specified host and 
# port, listen for incoming connections, accept a connection from the 
# client, receive a message, send back the same message to the client, 
# and then close the connection.
# - Client Program: The client should connect to the server using the 
# specified host and port, send a predefined message, wait for a 
# response from the server, print the received message to confirm it 
# matches the sent message, and then close the connection.
# Evaluation
# Submissions will be evaluated based on the following criteria:
# - The server must successfully start, accept a connection, correctly 
# receive and echo back the message received from the client, and then 
# close the connection.
# - The client must successfully connect to the server, send the 
# predefined message, correctly receive and verify the echoed message, 
# print the received message, and then close the connection.
# - Accuracy of the implemented protocol, ensuring that the message is 
# correctly sent, received, and echoed back.
# - Correct handling of network sockets, including opening and closing 
# connections properly.