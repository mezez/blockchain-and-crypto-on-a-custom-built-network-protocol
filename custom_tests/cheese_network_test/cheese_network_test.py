import queue
import unittest
from cheese_network.peer import Peer
from threading import Thread
import socket

class CheeseNetworkTest(unittest.TestCase):

    def test_handle_accept_all(self):
        q = queue.Queue()
        node_id = 1
        host = None
        port = None
        sample_peer = Peer(node_id, host, port)
        result = sample_peer.handle_accept_all(q)
        self.assertEqual(type(result), Thread)

    def test_connect_to_peer(self):
        node_id = 1
        host = None
        port = None
        sample_peer = Peer(node_id, host, port)
        result = sample_peer.connect_to_peer(sample_peer.peer_id, sample_peer.host, sample_peer.port)
        self.assertEqual(type(result), Thread)

    def test_connect_to_tracker(self):
        node_id = 1
        host = None
        port = None
        sample_peer = Peer(node_id, host, port)
        try:
            sample_peer.connect_to_tracker()
        except:
            self.fail("Exception in connect_to_tracker()")
        self.assertEqual(True, True)

    def test_handle_peers(self):
        node_id = 1
        host = '0.0.0.0' #'192.168.0.22'
        port = 5007
        sample_peer = Peer(node_id, host, port)
        my_queue = None
        peer_socket = socket.socket()
        peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server_socket.bind(('0.0.0.0', CheeseProtocol.TRACKER_PORT))
        peer_socket.bind((host, port))
        #peer_socket.listen()
        s = peer_socket.accept()

        result = sample_peer.handle_peers(s, my_queue)

        self.assertEqual(type(result), Thread)

    def test_request_connected_peers(self):
        node_id = 1
        host = '192.168.0.22' #'0.0.0.0'
        port = 5007
        sample_peer = Peer(node_id, host, port)
        result = sample_peer.request_connected_peers()
        if result == None:
            msg = "No connected Peers"
            self.assertEqual(result, None, msg)
        self.assertEqual(type(result), str)

    #def test_request_chain(self):

