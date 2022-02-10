import decimal
import queue
import random
import socket
import sys
import time

from threading import Thread

from my_helpers import MyHelpers
from cheese_protocol import CheeseProtocol


class Peer:

    def __init__(self, host, port):
        self.peer_id = None
        self.connected_peers = []
        self.tracker_socket = None
        self.host = host
        self.port = port
        self.connected_peers = []

        self.connect_to_tracker()

    @staticmethod
    def main_old():  # called at the end of the file
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

    def main(self):  # called at the end of the file

        # for storing clients requests
        q = queue.Queue()
        # start a new thread to accept new connections
        self.handle_accept_all(q).start()

    def handle_accept_all(self, my_queue):
        def handle():
            # create a socket that listens (on a port of your choice)
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # server_socket.bind(('0.0.0.0', CheeseProtocol.TRACKER_PORT))
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(server_socket)
            print('waiting for connection from other peers')

            # accept new peers connections,
            while True:
                s, addr = server_socket.accept()  # blocking
                print('received connection', s)

                # notify peer of successful connection
                connection_message = "Connected to peer: " + self.peer_id
                # s.send(connection_message.encode())
                s.send(connection_message)

                # and start a handle_client thread every time
                self.handle_peers(s, my_queue).start()

        t = Thread(target=handle)
        return t

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

                    if self.host is None or self.port is None:
                        sys.exit('You need a host and port to set up your socket and connect to tracker')

                    # set up your socket and start listening
                    if self.main():
                        join_request = CheeseProtocol.join_chain + "_:" + self.host + ":" + str(self.port)
                        Peer.send_message(join_request, self.tracker_socket)

                if line.startswith(MyHelpers.peer_id_start_string):
                    # peer id received
                    self.peer_id = line

        #s.close()

    def handle_peers(self, socket, my_queue):
        def handle():  # add elements to queue
            # initialise a random integer position, e.g. between 0 and 100

            # loop over the received data, ignoring (or just printing) this data for now (e.g., use netutils to read lines)
            # be sure to end the loop when the connection is closed (readLine returns None or throws an exception)
            while True:
                line = MyHelpers.read_line(socket)
                if line is None:
                    # remove client from connected peers
                    break
                else:
                    print("received", line)

                    """process request"""
                    request_type = CheeseProtocol.process_client_request(line)

                    if request_type == CheeseProtocol.join_chain:
                        peer_id = MyHelpers.generate_peer_id()
                        self.connected_peers.append(peer_id)
                        # send peer_id to client, id will be required for other requests
                        socket.send(peer_id)

                    if request_type == CheeseProtocol.get_peers:
                        connected_peers_sublist = MyHelpers.get_part_of_peers(self.connected_peers, True)
                        connected_peers_sublist = MyHelpers.connected_peers_start_string + connected_peers_sublist + '\r\n'
                        socket.send(connected_peers_sublist.encode())

        t = Thread(target=handle)
        return t

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
