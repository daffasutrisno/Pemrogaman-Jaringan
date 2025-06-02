import socket
import json
import sys
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO


def fetch_post_title():
    # Membuat koneksi socket ke jsonplaceholder.typicode.com pada port 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('jsonplaceholder.typicode.com', 80))
        
        # Mengirimkan HTTP GET request
        request = "GET /posts/1 HTTP/1.1\r\nHost: jsonplaceholder.typicode.com\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())
        
        # Menerima respons dari server
        response = s.recv(4096)
        
        # Mengambil data respons JSON
        response_data = response.decode().split('\r\n\r\n')[1]
        post_data = json.loads(response_data)
        
        # Mengembalikan judul post
        return post_data["title"]


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestHttpRequest(unittest.TestCase):
    @patch('socket.socket')
    def test_fetch_post_title(self, mock_socket):
        # Setup mock response
        sample_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"title\": \"sunt aut facere repellat provident occaecati excepturi optio reprehenderit\"}"
        
        # Setup mock socket instance
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        mock_sock_instance.recv.return_value = sample_response.encode()

        # Call function to fetch post title
        title = fetch_post_title()

        # Verifikasi bahwa mock socket melakukan panggilan sesuai harapan
        mock_socket.assert_called_once()
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        mock_sock_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        # Assert bahwa send dipanggil sekali dengan request yang benar
        mock_sock_instance.sendall.assert_called_once_with(b'GET /posts/1 HTTP/1.1\r\nHost: jsonplaceholder.typicode.com\r\nConnection: close\r\n\r\n')
        print(f"send called with: {mock_sock_instance.sendall.call_args}")

        # Assert bahwa recv dipanggil sekali untuk menerima data
        mock_sock_instance.recv.assert_called_once_with(4096)
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        # Verifikasi judul yang diterima dengan nilai yang diharapkan
        assert_equal(title, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit")


if __name__ == '__main__':
    # to run the script without unit test:
    # python solution.py run
    # if len(sys.argv) == 2 and sys.argv[1] == 'run':
    #     title = fetch_post_title()
    #     print(title)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
