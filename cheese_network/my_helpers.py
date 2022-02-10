import json
import uuid
import random


class MyHelpers:

    peer_id_start_string = "PID"
    connected_peers_start_string = "CPSS"

    @staticmethod
    def verify_peer_id(peer_id, peers):
        if peer_id in peers:
            return peers.index(peer_id)
        return False

    @staticmethod
    def custom_read(f):
        data = f.recv(1024).decode()
        return data

    @staticmethod
    def read_line(f):
        res = b""
        was_r = False
        while True:
            b = f.recv(1)
            if len(b) == 0:
                return None
            if b == b"\n" and was_r:
                break
            if was_r:
                res += b"\r"
            if b == b"\r":
                was_r = True
            else:
                was_r = False
                res += b
        return res.decode("utf-8")

    @staticmethod
    def generate_peer_id():
        peer_id = MyHelpers.peer_id_start_string + uuid.uuid5(uuid.NAMESPACE_URL, 'mez').hex
        return peer_id

    @staticmethod
    def get_part_of_peers(connected_peers, convert_to_string=False):
        if len(connected_peers) <= 10:
            if convert_to_string is True:
                return json.dumps(connected_peers)
            return connected_peers

        # randomly select a part of the list, containing 10 peers
        connected_peers_sublist = random.sample(connected_peers, 10)
        if convert_to_string is True:
            return json.dumps(connected_peers_sublist)
        return connected_peers_sublist
