import socket
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

# Server functionality
def handle_client_connection(client_socket, addr):
    """Handle a single client connection."""
    print(f"Got a connection from {addr}")
    
    # send message
    client_socket.send(b'Hello, Client!')

    # close socket
    client_socket.close()

def start_server():
    """Start the server and listen for incoming connections."""
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # define the address
    host = '127.0.0.1'        # Localhost
    port = 12345        # Port to listen on
    
    # bind to address
    server_socket.bind((host, port))

    # listen
    server_socket.listen(1)
    print(f"Listening on {host}:{port} ...")
    
    try:
        while True:
            # accept connection
            client_socket, addr = server_socket.accept()

            # handle client connection 
            handle_client_connection(client_socket, addr)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # close socket
        server_socket.close()


class ExitLoopException(Exception):
    pass

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

# Unit test for server
class TestServer(unittest.TestCase):
    @patch('socket.socket')
    def test_handle_client_connection(self, mock_socket):
        """Test handling of a client connection."""
        print('Test handle_client_connection ...')
        mock_client_socket = MagicMock()
        mock_addr = ('127.0.0.1', 12345)
        handle_client_connection(mock_client_socket, mock_addr)
        
        mock_client_socket.send.assert_called_with(b'Hello, Client!')
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
        # Use ExitLoopException to exit the loop after simulating a single client connection
        mock_server_socket.accept.side_effect = [(mock_client_socket, mock_addr), ExitLoopException]
        
        # Run start_server and catch the custom ExitLoopException to exit the test cleanly
        try:
            start_server()
            
            # Ensure the loop was exited due to the ExitLoopException
            mock_server_socket.accept.assert_called()
            
        except ExitLoopException:
            pass  # Loop exited as expected
    
        print(f"accept called with: {mock_server_socket.accept.call_args}")

        # Assertions to verify the server setup
        mock_server_socket.bind.assert_called_once_with(('127.0.0.1', 12345))
        print(f"bind called with: {mock_server_socket.bind.call_args}")

        mock_server_socket.listen.assert_called_once_with(1)
        print(f"listen called with: {mock_server_socket.listen.call_args}")


if __name__ == '__main__':
    # Run unittest with a custom runner that suppresses output
    # Make sure to uncomment this before uploading the code to domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

    # Uncomment this if you want to run the client program, not running the unit test
    # start_server()



#     Server-Client Communication (Server)
# Description
# In this problem, you are asked to test the 
# interaction between a server and a client through 
# socket programming. The server will send a greeting 
# message to the client, and the client should receive 
# this message correctly.
# Input
# There is no input for this problem as the interaction 
# happens over a network connection established between 
# the server and the client. The server will listen on 
# localhost (127.0.0.1) at port 12345 and send a 
# specific message to the client upon connection.
# Output
# The client should output the message received from 
# the server to the standard output. The complete 
# output of program is as follows (you do not need to 
# write the unit test as it is provided in the 
# skeleton):
# - Server output:
# Test handle_client_connection ...
# Got a connection from ('127.0.0.1', 12345)
# send called with: call(b'Hello, Client!')
# close called with: call()
# Test start_server ...
# Listening on 127.0.0.1:12345 ...
# Got a connection from ('127.0.0.1', 12345)
# accept called with: call()
# bind called with: call(('127.0.0.1', 12345))
# listen called with: call(1)
# Method
# Your task is to implement and run both the server and 
# client programs as provided. Ensure the client 
# successfully connects to the server, receives the 
# message, and prints the exact expected output.
# - Server Program: The server should start, bind to 
# the specified localhost and port, listen for incoming 
# connections, accept a client connection, send the 
# message "Hello, Client!", and then close the 
# connection. It must handle a single client connection 
# before shutting down for the purpose of this problem.
# - Client Program: The client should connect to the 
# server's specified host and port, receive the message 
# from the server, print the received message in the 
# specified format, and then close the connection.
# Evaluation
# The submission will be evaluated based on the 
# following criteria:
# - The server must successfully start, send the 
# correct message to the client, and close the 
# connection.
# - The client must successfully connect to the server, 
# receive the message, and print the output in the 
# specified format.
# - The use of unit tests for both server and client to 
# ensure the correct behavior of sending and receiving 
# the message.