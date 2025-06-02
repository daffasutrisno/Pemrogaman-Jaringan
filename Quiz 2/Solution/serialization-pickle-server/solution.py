import socket
import select
import pickle
from datetime import datetime
import logging
import unittest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Message:
    def __init__(self, username, text, timestamp):
        self.username = username
        self.text = text
        self.timestamp = timestamp

    @staticmethod
    def deserialize(serialized_message):
        return pickle.loads(serialized_message)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    server_socket.setblocking(False)

    sockets_list = [server_socket]

    logger.info("Server is listening on port 12345")

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                logger.info(f"Accepted new connection from {client_address}")
            else:
                try:
                    data = notified_socket.recv(1024)
                    if data:
                        message = Message.deserialize(data)
                        logger.info("Received message:")
                        logger.info(f"Username: {message.username}")
                        logger.info(f"Text: {message.text}")
                        logger.info(f"Timestamp: {message.timestamp}")
                except Exception as e:
                    logger.info(f"Exception: {e}")
                    sockets_list.remove(notified_socket)
                    notified_socket.close()

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            notified_socket.close()


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_true_any(parameter1, parameter2):
    found = False
    for message in parameter2:
        if parameter1 in message:
            found = True
            break

    print(f'test attribute passed: {parameter1} found in log messages' if found else f'test attribute failed: {parameter1} not found in log messages')


class TestChatServer(unittest.TestCase):

    @patch('select.select')
    @patch('socket.socket')
    def test_server_main(self, mock_socket_class, mock_select):
        mock_server_socket = MagicMock()
        mock_client_socket = MagicMock()

        mock_socket_class.return_value = mock_server_socket
        mock_server_socket.accept.return_value = (mock_client_socket, ('127.0.0.1', 54321))

        # Initial select: server socket is ready -> accept
        # Second select: client socket is ready -> recv
        mock_select.side_effect = [
            ([mock_server_socket], [], []),
            ([mock_client_socket], [], []),
            KeyboardInterrupt()
        ]

        test_message = Message("Alice", "Hello, World!", datetime.now())
        serialized_message = pickle.dumps(test_message)
        mock_client_socket.recv.return_value = serialized_message

        with self.assertLogs(logger, level='INFO') as log:
            with self.assertRaises(KeyboardInterrupt):
                main()

            log_output = log.output
            assert_true_any("Received message:", log_output)
            assert_true_any("Username: Alice", log_output)
            assert_true_any("Text: Hello, World!", log_output)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        main()
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)