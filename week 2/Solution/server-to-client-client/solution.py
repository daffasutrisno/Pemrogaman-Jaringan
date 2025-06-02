import socket
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

# Client functionality
def client_program():
    host = "127.0.0.1"
    port = 12345

    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    client_socket.connect((host, port))

    # receive message
    message = client_socket.recv(1024)
    print(f"Received from server: {message.decode()}")

    # close socket
    client_socket.close()

# Unit test for the client code
class TestClient(unittest.TestCase):
    @patch('socket.socket')  # Mock the socket object
    def test_client_program(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        # Mock the server's response to "Hello, Client!"
        mock_socket_instance.recv.return_value = b'Hello, Client!'

        client_program()  # Run the client program

        # Verify connection to the correct server and port
        mock_socket_instance.connect.assert_called_with(('127.0.0.1', 12345))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        # Verify the client receives a message
        mock_socket_instance.recv.assert_called_with(1024)
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        # Verify the client closes the socket after receiving the message
        mock_socket_instance.close.assert_called_once()
        print(f"close called with: {mock_socket_instance.close.call_args}")

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

if __name__ == '__main__':
    # Run unittest with a custom runner that suppresses output
    # Make sure to uncomment this before uploading the code to domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

    # Uncomment this if you want to run the client program, not running the unit test
    # client_program()



#     Server Sends Message to Client (Client)
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
# the server to the standard output. The expected 
# message is: Received from server: Hello, Client!
# In addition, the complete output of the client is as 
# follows (you do not need to write the unit test as it 
# is provided in the skeleton):
# Received from server: Hello, Client!
# connect called with: call(('127.0.0.1', 12345))
# recv called with: call(1024)
# close called with: call()
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