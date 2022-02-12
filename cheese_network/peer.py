import decimal
import queue
import random
import socket
import sys
import time

from threading import Thread

from cheese_network.my_helpers import MyHelpers
from cheese_network.cheese_protocol import CheeseProtocol
from wallet import Wallet


class Peer:

    def __init__(self, host=None, port=None):
        self.peer_id = None
        self.connected_peers = []
        self.tracker_socket = None
        self.host = host
        self.port = port
        self.connected_to = []
        self.wallet = Wallet()

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
        return True

    def handle_accept_all(self, my_queue):
        def handle():
            # create a socket that listens (on a port of your choice)
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # server_socket.bind(('0.0.0.0', CheeseProtocol.TRACKER_PORT))
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print('My listening socket')
            print(server_socket)
            print('waiting for connection from other peers')

            # accept new peers connections,
            while True:
                s, addr = server_socket.accept()  # blocking
                print('received connection', s)

                # notify peer of successful connection
                connection_message = "Connected to peer: " + self.peer_id
                s.send(connection_message.encode())

                # and start a handle_peer thread every time
                self.handle_peers(s, my_queue).start()

        t = Thread(target=handle)
        return t

    def request_cheesechain_from_peers(self):
        # loop through connected peers list and request for cheesechain from them all
        pass

    # spin up a thread everytime you connect to a peer
    def connect_to_peer(self, peer_id, peer_host, peer_port):
        def handle_connect():
            print("Connecting to peer" + str(peer_id))
            s = socket.create_connection((peer_host, peer_port))
            self.tracker_socket = s
            print("created", s)
            # Connection Successful, spin up a thread to handle there requests
            self.handle_peers(self, s).start()

            # update list of peers you connected to
            peer_info = {
                'peer_id': peer_id,
                'host': peer_host,
                'post': peer_port
            }
            self.connected_to.append(peer_info)

            # while True:
                #line = MyHelpers.read_line(socket)
                #if line is None:
                    # end the loop when the connection is closed (readLine returns None or throws an exception)
                 #   break
                #else:
                 #   print("received", line)
                  #  if line.startswith("Connected to peer:"):
                   #     print(line)

                    # action for receiving newly mined cheese notification from peer
                    # maybe the broadcast should come with the cheesechain and open transactions


                    # action for receiving cheesechain from peers

            #s.close()
        t = Thread(target=handle_connect)
        return t

    def connect_to_tracker(self):
        print("Connecting to tracker")
        s = socket.create_connection((CheeseProtocol.TRACKER_HOST, CheeseProtocol.TRACKER_PORT))
        self.tracker_socket = s
        print("created", s)

        my_info = s.getsockname()
        self.host = my_info[0]
        self.port = my_info[1]
        print("my host", self.host)
        print("my port", self.port)

        # Connection Successful, spin up a thread to handle there requests
        # self.handle_peers(self, s).start()
        initial_listening = True
        while initial_listening:
            # line = MyHelpers.read_line(s)
            line = MyHelpers.custom_read(s)
            if line is None:
                # end the loop when the connection is closed (readLine returns None or throws an exception)
                print("No response received")
                break
            else:
                print("RECEIVED LINE:")
                print("received", line)
                if line == "Connection Successful":
                    # request to join chain

                    if self.host is None or self.port is None:
                        sys.exit('You need a host and port to set up your socket and connect to tracker')

                    # set up your socket and start listening
                    if self.main():
                        print("IN MAIN:")
                        join_request = CheeseProtocol.join_chain + "_:" + self.host + ":" + str(self.port)
                        Peer.send_message(join_request, self.tracker_socket)

                if line.startswith(MyHelpers.peer_id_start_string):
                    # peer id received
                    print("IN peer id:")
                    self.peer_id = line

                    # once peer id is received, spin up a thread to listen  and
                    # to other things that may come from the tracker
                    # but don't close the connection
                    initial_listening = False
                    # return self.__dict__

        #handle subsequent messages from tracker
        #s.close()

    # peers connected to you and the ones you connected to
    def handle_peers(self, socket, my_queue=None):
        def handle():

            # loop over the received data, ignoring (or just printing) this data for now (e.g., use netutils to read lines)
            # be sure to end the loop when the connection is closed (readLine returns None or throws an exception)
            while True:
                line = MyHelpers.read_line(socket)
                if line is None:
                    # remove client from connected peers
                    break
                else:
                    print("received", line)

                    if line.startswith("Connected to peer:"):
                        print(line)

                    """process request requests received from peers,"""
                    request_type = CheeseProtocol.process_peer_request(line)

                    if request_type == CheeseProtocol.get_chain:
                        # load node, retrieve wallet and get cheesechain and open transactions from it
                        # convert to string and sent to peer
                        pass

                    if request_type == CheeseProtocol.new_cheese:
                        pass


        t = Thread(target=handle)
        return t

    def request_connected_peers(self):
        print(self.tracker_socket)
        if self.peer_id is not None and self.tracker_socket is not None:
            request = CheeseProtocol.get_peers + ':' + self.peer_id
            Peer.send_message(request, self.tracker_socket)

            listening_for_response = True
            connected_peers = None
            while listening_for_response:
                line = MyHelpers.custom_read(self.tracker_socket)
                if line is None:
                    # end the loop when the connection is closed (readLine returns None or throws an exception)
                    print("No response received")
                    break
                    #pass
                else:
                    print("RECEIVED LINE:")
                    print("received", line)
                    if line.startswith(MyHelpers.connected_peers_start_string):
                        print('CONNECTED PEERS')
                        connected_peers = line
                        listening_for_response = False
            return connected_peers
        else:
            return False

    def request_chain(self):
        pass

    def share_cheesechain(self):
        pass

    def share_new_cheeschain(self):
        pass

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
