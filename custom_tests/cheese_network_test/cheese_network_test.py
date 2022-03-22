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
        """TO RUN THIS SUCCESSFULLY, YOU NEED TO HAVE THE TRACKER RUNNING"""
        node_id = 1
        host = None
        port = None
        sample_peer = Peer(node_id, host, port)
        try:
            sample_peer.connect_to_tracker()
        except:
            self.fail("Exception in connect_to_tracker()")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()