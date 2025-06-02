import socket
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

def client_program():
    host = '127.0.0.1'
    port = 12345

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to server
    client_socket.connect((host, port))

    # Sending message
    message = b'Welcome into this client-server-client sending message program!'
    client_socket.send(message)
    print(f"Sending to server: {message.decode()}")

    # Receive back the message (response)
    response = client_socket.recv(1024)
    print(f"Received back from server: {response.decode()}")

    # Close the socket
    client_socket.close()

class TestClient(unittest.TestCase):
    @patch('socket.socket')
    def test_client_program(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        mock_socket_instance.recv.side_effect = [
            b'Welcome into this client-server-client sending message program!'
        ]

        client_program()

        mock_socket_instance.connect.assert_called_with(('127.0.0.1', 12345))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_with(b'Welcome into this client-server-client sending message program!')
        print(f"send called with: {mock_socket_instance.send.call_args}")

        mock_socket_instance.recv.assert_called_with(1024)
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        mock_socket_instance.close.assert_called_once()
        print(f"close called with: {mock_socket_instance.close.call_args}")

class NullWriter(StringIO):
    def write(self, txt):
        pass

if __name__ == '__main__':
    # Run unittest with a custom runner that suppresses output
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)

    # Uncomment this if you want to run the client program, not running the unit test
    # client_program()



#     Echo Server (Client)
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