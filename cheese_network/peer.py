import ast
import decimal
import json
import queue
import random
import socket
import struct
import sys
import time

from threading import Thread

from cheese_network.my_helpers import MyHelpers
from cheese_network.cheese_protocol import CheeseProtocol
from wallet import Wallet
from cheesechain import Cheesechain


class Peer:

    def __init__(self, node_id, host=None, port=None):
        self.peer_id = None
        self.connected_peers = None
        self.tracker_socket = None
        self.host = host
        self.port = port
        self.node_id = node_id
        self.connected_to = []
        self.wallet = Wallet(node_id)

        self.connect_to_tracker()

    def main(self):  # called at the end of the file

        # for storing clients requests
        q = queue.Queue()
        # start a new thread to accept new connections
        self.handle_accept_all(q).start()
        return True

    def handle_accept_all(self, my_queue):
        def handle():
            # create a socket that listens (on a port of your choice)
            peer_socket = socket.socket()
            peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # server_socket.bind(('0.0.0.0', CheeseProtocol.TRACKER_PORT))
            peer_socket.bind((self.host, self.port))
            peer_socket.listen()
            print('My listening socket')
            print(peer_socket)
            print('waiting for connection from other peers')

            # accept new peers connections,
            while True:
                s, addr = peer_socket.accept()  # blocking
                print('received connection', s)

                # notify peer of successful connection
                connection_message = CheeseProtocol.PCONNECTACK + ":" + self.peer_id
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
                'port': peer_port
            }
            self.connected_to.append(peer_info)

            # while True:
            # line = MyHelpers.read_line(socket)
            # if line is None:
            # end the loop when the connection is closed (readLine returns None or throws an exception)
            #   break
            # else:
            #   print("received", line)
            #  if line.startswith("Connected to peer:"):
            #     print(line)

            # action for receiving newly mined cheese notification from peer
            # maybe the broadcast should come with the cheesechain and open transactions

            # action for receiving cheesechain from peers

            # s.close()

        t = Thread(target=handle_connect)
        return t

    def connect_to_tracker(self):
        print("Connecting to tracker")
        print("host", CheeseProtocol.TRACKER_URL)
        print("port", CheeseProtocol.TRACKER_PORT)
        # s = socket.create_connection((CheeseProtocol.TRACKER_HOST, CheeseProtocol.TRACKER_PORT))
        s = socket.create_connection((CheeseProtocol.TRACKER_URL, CheeseProtocol.TRACKER_PORT))
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
                    # request to join chain network
                    if self.host is None or self.port is None:
                        sys.exit('You need a host and port to set up your socket and connect to tracker')

                    # set up your socket and start listening
                    if self.main():
                        print("IN MAIN:")
                        join_request = CheeseProtocol.PCONNECT + ":" + self.host + ":" + str(self.port)
                        Peer.send_message(join_request, self.tracker_socket)

                # if line.startswith(MyHelpers.peer_id_start_string):
                if line.startswith(CheeseProtocol.TCONNECTRESP):
                    # peer id received
                    print("IN peer id:")
                    request_body = line.split(':')
                    pid = request_body[1]
                    self.peer_id = pid

                    # once peer id is received, spin up a thread to listen  and
                    # to other things that may come from the tracker
                    # but don't close the connection
                    initial_listening = False
                    # return self.__dict__

        # handle subsequent messages from tracker
        # s.close()

    # peers connected to you and the ones you connected to
    def handle_peers(self, socket, my_queue=None):
        def handle():

            # loop over the received data, ignoring (or just printing) this data for now (e.g., use netutils to read lines)
            # be sure to end the loop when the connection is closed (readLine returns None or throws an exception)
            while True:
                line = MyHelpers.custom_read(socket)
                if line is None:
                    # remove client from connected peers
                    break
                else:
                    print("received", line)

                    if line.startswith(CheeseProtocol.PCONNECTACK):
                        print(line)

                    """process request requests received from peers,"""
                    request_type = CheeseProtocol.process_peer_request(line)

                    if request_type == CheeseProtocol.GETCHAIN:
                        # load node, retrieve wallet and get cheesechain
                        request_body = line.split(':')
                        node_id = self.node_id

                        # maybe this is not even needed, walled is initialized when peer starts
                        wallet = Wallet(node_id)

                        wallet.load_keys()
                        cheesechain = Cheesechain(wallet.public_key, node_id)
                        chain = MyHelpers.get_peer_chain(cheesechain)
                        print('RETRIEVED CHAIN')
                        print(chain)

                        # convert to string and send to peer
                        formatted_chain = CheeseProtocol.GETCHAINRESP + chain
                        socket.sendall(formatted_chain.encode())

                    if request_type == CheeseProtocol.GETOPENTRANSACTIONS:
                        # load node, retrieve wallet and get open transactions
                        request_body = line.split(':')
                        node_id = self.node_id

                        # maybe this is not even needed, walled is initialized when peer starts
                        wallet = Wallet(node_id)
                        wallet.load_keys()
                        cheesechain = Cheesechain(wallet.public_key, node_id)
                        transactions = MyHelpers.get_peer_open_transactions(cheesechain)
                        print('RETRIEVED TRANSACTIONS')
                        print(transactions)

                        # convert to string and send to peer
                        formatted_tr = CheeseProtocol.GETOPENTRANSACTIONSRESP + transactions
                        socket.sendall(formatted_tr.encode())

                    if request_type == CheeseProtocol.BRCHEESE:
                        # TODO add_cheese_from_remote_peer(cheese)
                        # compare with your local chain and update if applicable
                        # maybe reject if invalid
                        request_body = line.split(';')
                        cheese = request_body[0].replace(CheeseProtocol.BRCHEESE, '')
                        print('CHEESE TO BROADCAST')
                        print(cheese)
                        cheese = ast.literal_eval(cheese)

                        """EITHER: if this peer will not also re broadcast to its peers, avoiding a chain reaction"""
                        node_id = self.node_id

                        # maybe this is not even needed, walled is initialized when peer starts
                        wallet = Wallet(node_id)
                        wallet.load_keys()
                        cheesechain = Cheesechain(wallet.public_key, node_id)
                        added = cheesechain.add_cheese(cheese)
                        print('ADD ATTEMPT COMPLETE')

                        """OR: if this peer will also re broadcast to its peers, leading to a chain reaction"""
                        # hopefully the node module will already be set up by the time this event occurs lol
                        # alternative: sending a pointer to add_cheese_from_remote_peer from source tr add point
                        # from node import add_cheese_from_remote_peer
                        # add_cheese_from_remote_peer(cheese)

                        res = CheeseProtocol.BRTRANSACTIONACK
                        socket.sendall(res.encode())
                    if request_type == CheeseProtocol.BRCHEESEACK:
                        # TODO SEND DISCONNECTION MESSAGE
                        socket.close()

                    if request_type == CheeseProtocol.BRTRANSACTION:
                        # TODO
                        # verify and compare with your local transactions and update if applicable
                        # maybe reject if invalid
                        request_body = line.split(':')
                        tr = request_body[0].replace(CheeseProtocol.BRTRANSACTION, '')
                        tr = ast.literal_eval(tr)

                        # peer_object = request_body[1]
                        # connected_peers = request_body[2]

                        """EITHER: if this peer will not also re broadcast to its peers, avoiding a chain reaction"""
                        node_id = self.node_id

                        # maybe this is not even needed, walled is initialized when peer starts
                        wallet = Wallet(node_id)
                        wallet.load_keys()
                        cheesechain = Cheesechain(wallet.public_key, node_id)
                        added = cheesechain.add_transaction(tr['recipient'], tr['sender'], tr['signature'],
                                                            tr['amount'])

                        """OR: if this peer will also re broadcast to its peers, leading to a chain reaction"""
                        # hopefully the node module will already be set up by the time this event occurs lol
                        # alternative: sending a pointer to add_transaction_from_remote_peer from source tr add point
                        # from node import add_transaction_from_remote_peer
                        # add_transaction_from_remote_peer(tr)

                        res = CheeseProtocol.BRTRANSACTIONACK
                        socket.sendall(res.encode())

                    if request_type == CheeseProtocol.BRTRANSACTIONACK:
                        # TODO SEND DISCONNECTION MESSAGE
                        socket.close()
                    if request_type == CheeseProtocol.HCK:
                        res = CheeseProtocol.HCKACK
                        socket.sendall(res.encode())

        t = Thread(target=handle)
        return t

    def request_connected_peers(self):
        print(self.tracker_socket)
        # if self.connected_peers is not None:
        # return self.connected_peers
        if self.peer_id is not None and self.tracker_socket is not None:
            request = CheeseProtocol.GETPEERS + ':' + self.peer_id
            Peer.send_message(request, self.tracker_socket)

            listening_for_response = True
            connected_peers = None
            while listening_for_response:
                line = MyHelpers.custom_read(self.tracker_socket)
                if line is None:
                    # end the loop when the connection is closed (readLine returns None or throws an exception)
                    print("No response received")
                    break
                    # pass
                else:
                    print("RECEIVED LINE (CONNECTED PEERS):")
                    print("received", line)
                    if line.startswith(CheeseProtocol.GETPEERSRESP):
                        connected_peers = line
                        listening_for_response = False
                        self.connected_peers = connected_peers
            return connected_peers
        else:
            return False

    def request_chain(self, peer_socket):
        if self.peer_id is not None:
            request = CheeseProtocol.GETCHAIN + ':' + self.peer_id
            Peer.send_message(request, peer_socket)

            listening_for_response = True
            peer_chain = None
            while listening_for_response:
                line = MyHelpers.custom_read(peer_socket)
                if line is None:
                    # end the loop when the connection is closed (readLine returns None or throws an exception)
                    print("No response received")
                    break
                    # pass
                else:
                    print("RECEIVED LINE (PEER CHAIN):")
                    print("received", line)
                    if line.startswith(CheeseProtocol.GETCHAINRESP):
                        peer_chain = line
                        listening_for_response = False
            return peer_chain
        else:
            return False

    def request_open_transactions(self, peer_socket):
        if self.peer_id is not None:
            request = CheeseProtocol.GETOPENTRANSACTIONS + ':' + self.peer_id
            Peer.send_message(request, peer_socket)

            listening_for_response = True
            peer_tr = None
            while listening_for_response:
                line = MyHelpers.custom_read(peer_socket)
                if line is None:
                    # end the loop when the connection is closed (readLine returns None or throws an exception)
                    print("No response received")
                    break
                    # pass
                else:
                    print("RECEIVED LINE (PEER TR):")
                    print("received", line)
                    if line.startswith(CheeseProtocol.GETOPENTRANSACTIONSRESP):
                        peer_tr = line
                        listening_for_response = False
            return peer_tr
        else:
            return False

    def share_cheese(self, cheese, peer_socket, peer_object):
        request = CheeseProtocol.BRCHEESE + json.dumps(cheese) + ';' + self.peer_id
        Peer.send_message(request, peer_socket)
        # spin up thread to wait for response and close connection afterwards
        peer_object.handle_peers(peer_socket)
        # listening_for_response = True
        # while listening_for_response:
        #     line = MyHelpers.custom_read(self.tracker_socket)
        #     if line is None:
        #         # end the loop when the connection is closed (readLine returns None or throws an exception)
        #         print("No response received")
        #         break
        #         # pass
        #     else:
        #         print("RECEIVED LINE (PEER TR):")
        #         print("received", line)
        #         if line.startswith(CheeseProtocol.BRTRANSACTIONACK):
        #             listening_for_response = False
        return True

    def share_new_cheesechain(self):
        pass

    def share_added_transaction(self, transaction, peer_socket, peer_object):
        request = CheeseProtocol.BRTRANSACTION + json.dumps(transaction) + ':' + self.peer_id
        Peer.send_message(request, peer_socket)
        # spin up thread to wait for response and close connection afterwards
        peer_object.handle_peers(peer_socket)
        # listening_for_response = True
        # while listening_for_response:
        #     line = MyHelpers.custom_read(self.tracker_socket)
        #     if line is None:
        #         # end the loop when the connection is closed (readLine returns None or throws an exception)
        #         print("No response received")
        #         break
        #         # pass
        #     else:
        #         print("RECEIVED LINE (PEER TR):")
        #         print("received", line)
        #         if line.startswith(CheeseProtocol.BRTRANSACTIONACK):
        #             listening_for_response = False
        return True

    def disconnect_from_peer(self):
        pass

    def disconnect_from_tracker(self):
        pass

    @staticmethod
    def send_magic_word(my_socket):
        # s.sendall(b'HI FROM SIMPLE CLIENT\r\n')
        my_socket.send(b'magic\r\n')
        print("sent magic word")

    @staticmethod
    def send_message(message, my_socket):
        # message = message + '\r\n'
        message = message.encode()
        # my_socket.send(message)
        my_socket.sendall(message)

    @staticmethod
    def send_messageOlder(message, my_socket):
        # Prefix each message with a 4-byte length (network byte order)
        message = struct.pack('>I', len(message)) + message
        my_socket.sendall(message)

    @staticmethod
    def send_message_old(message, my_socket):
        total_sent = 0
        while total_sent < len(message):
            sent = my_socket.send(message[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent


if __name__ == "__main__":
    pass
    # Peer.main()
