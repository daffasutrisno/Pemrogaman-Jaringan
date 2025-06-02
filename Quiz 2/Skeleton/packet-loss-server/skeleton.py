import ??


def start_server():
    # Define the host and port
    host = ? 
    port = ? 

    # Create a UDP socket and bind it to the address
    server_socket = ?  

    print(??)

    try:
        message = ""
        i = 0
        client_addr = None

        while True:
            # Receive one byte from client
            data, addr = ? 

            # Exit if no data
            if not data:
                break

            # Store client address
            client_addr = addr

            # Decode the received byte to a character
            char = ?  # data.decode(...)

            # Check if this is the end-of-message signal

            # Drop every 10th packet

            i += 1

        # Send the reconstructed message back to client
        if client_addr:
            ? 
            print(??)

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # Close socket
        ??


class ExitLoopException(Exception):
    pass


class NullWriter(StringIO):
    def write(self, txt):
        pass


class TestUDPServer(unittest.TestCase):
    @patch("socket.socket")
    def test_udp_packet_drop_logic(self, mock_socket_cls):
        host = "127.0.0.1"
        port = 9876

        # Mock socket
        mock_socket = MagicMock()
        mock_socket_cls.return_value = mock_socket

        # The original message sent character by character
        message = (
            "K^sXjF@WeuQ{=nZrGMdVYtc#]Pk|a?o>Rb&Lq(ASz$Tw}iC+MJ*<!gHEhBfNUOdy" + "\0"
        )
        sent_bytes = [c.encode() for c in message]

        recv_sequence = [(b, (host, 50062)) for b in sent_bytes]
        mock_socket.recvfrom.side_effect = recv_sequence

        # Capture the printed output
        captured_output = StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured_output
        try:
            start_server()
        finally:
            sys.stdout = sys_stdout

        output = captured_output.getvalue()
        # print(output)

        # ✅ Check socket creation as UDP
        mock_socket_cls.assert_called_with(socket.AF_INET, socket.SOCK_DGRAM)
        print("✅ Used UDP socket")

        # ✅ Check bind to correct address
        mock_socket.bind.assert_called_with((host, port))
        print("✅ Bound to address (127.0.0.1, 9876)")

        # ✅ Check correct dropped/kept messages printed
        self.assertIn("[Server] Dropping packet index 0: 'K'", output)
        self.assertIn("[Server] Dropping packet index 10: 'Q'", output)
        self.assertIn("[Server] Dropping packet index 20: 'Y'", output)
        self.assertIn("[Server] Dropping packet index 30: 'o'", output)
        self.assertIn("[Server] Dropping packet index 40: 'z'", output)
        self.assertIn("[Server] Dropping packet index 50: '*'", output)
        self.assertIn("[Server] Dropping packet index 60: 'U'", output)
        print("✅ Printed expected dropped/kept packet logs")

        # ✅ Check final message sent to client is correct (excluding dropped characters)
        expected_sent_back = "".join(
            message[i]
            for i in range(len(message))
            if message[i] != "\0" and i % 10 != 0
        )
        sent_data, _ = mock_socket.sendto.call_args[0]
        self.assertEqual(sent_data.decode(), expected_sent_back)
        print("✅ Sent correct response message back to client")

        # ✅ Check transmission end and response log
        self.assertIn("[Server] End-of-transmission signal received.", output)
        self.assertIn("[Server] Sent response to ('127.0.0.1', 50062)", output)
        print("✅ test_udp_packet_drop_logic passed all checks")


if __name__ == "__main__":
    # start_server()

    # run unit test
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
