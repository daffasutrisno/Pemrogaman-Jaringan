import ??

def send_packet():
    # Create a UDP socket
    client_socket = 

    try:
        host = ??
        port = ??

        print(??)

        message = ??

        # Send each character one by one
            ??

        # Receive one UDP packet (server sends all at once)
        part, _ = ??
        received_message = ??

        print(??)
        print(??)

        # Compare to original message to find lost characters
        received_index = 0
        lost_chars = ??
        for char in message:
            if (??):
                ??
            else:
                ??
        
        print(??)
        print(??)

    finally:        
        # Close socket
        ??
        print(??)


class NullWriter(StringIO):
    def write(self, txt):
        pass


# Unit tests
class TestUDPPacket(unittest.TestCase):
    @patch("socket.socket")
    def test_send_packet_udp(self, mock_socket_cls):
        host = "127.0.0.1"
        port = 9876

        # Create mock socket and simulate it being returned from socket.socket()
        mock_socket = MagicMock()
        mock_socket_cls.return_value = mock_socket

        # Simulated response from the server
        received_message = "^sXjF@Weu{=nZrGMdVtc#]Pk|a?>Rb&Lq(AS$Tw}iC+MJ<!gHEhBfNOdy"
        expected_lost = "KQYoz*U"
        mock_socket.recvfrom.return_value = (received_message.encode(), (host, port))

        # Capture printed output
        captured_output = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            send_packet()
        finally:
            sys.stdout = sys_stdout
            # print(captured_output.getvalue())

        output = captured_output.getvalue()

        # ✅ Check that the socket was created as a UDP socket
        mock_socket_cls.assert_called_with(socket.AF_INET, socket.SOCK_DGRAM)
        print("✅ Used UDP socket")

        # ✅ Check that sendto was called with correct host/port
        self.assertTrue(
            all(
                call[0][1] == (host, port) for call in mock_socket.sendto.call_args_list
            ),
            "All sendto() calls should target the correct (host, port)",
        )
        print("✅ All sendto() calls used correct server address")

        # ✅ Check output content
        self.assertIn("Connected to server on port 9876", output)
        self.assertIn(received_message, output)
        self.assertIn("Lost characters:", output)
        self.assertIn(expected_lost, output)
        self.assertIn("Connection closed.", output)

        print("✅ Output matched expected lost characters")
        print("✅ test_send_packet_udp passed all checks")


if __name__ == "__main__":
    # send_packet()
    # run unit test
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
