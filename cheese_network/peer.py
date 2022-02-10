import decimal
import random
import socket
import time

from my_helpers import MyHelpers
from cheese_protocol import CheeseProtocol


class Peer:

    def __init__(self):
        self.peer_id = None
        self.connected_peers = []
        self.tracker_socket = None

        self.connect_to_tracker()

    @staticmethod
    def main(self):  # called at the end of the file
        print("Creating connection")
        s = socket.create_connection(('localhost', CheeseProtocol.TRACKER_PORT))
        print("created", s)

        message_count = 0
        while message_count < 50:
            time.sleep(decimal.Decimal(random.randrange(1, 99)) / 100)
            Peer.send_magic_word(s)
            message_count = message_count + 1

        s.close()

        # while True:
        #     l = netutils.read_line(s)
        #     print("got reply:", l)

    def connect_to_tracker(self):
        print("Connecting to tracking")
        s = socket.create_connection(('localhost', CheeseProtocol.TRACKER_PORT))
        self.tracker_socket = s
        print("created", s)

        # Connection Successful
        while True:
            line = MyHelpers.read_line(socket)
            if line is None:
                # end the loop when the connection is closed (readLine returns None or throws an exception)
                break
            else:
                print("received", line)
                if line == "Connection Successful":
                    # request to join chain
                    Peer.send_message(CheeseProtocol.join_chain)

                if line.startswith(MyHelpers.peer_id_start_string):
                    # peer id received
                    self.peer_id = line

        #s.close()

    def request_connected_peers(self):
        if self.peer_id is not None and self.tracker_socket is not None:
            Peer.send_message(CheeseProtocol.get_peers, self.tracker_socket)
        else:
            return False

    @staticmethod
    def send_magic_word(my_socket):
        # s.sendall(b'HI FROM SIMPLE CLIENT\r\n')
        my_socket.send(b'magic\r\n')
        print("sent magic word")

    @staticmethod
    def send_message(message, my_socket):
        message = message + '\r\n'
        message = message.encode()
        my_socket.send(message)


if __name__ == "__main__":
    Peer.main()
