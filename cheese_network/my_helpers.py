import json
import struct
import sys
import uuid
import random


class MyHelpers:

    peer_id_start_string = "PID"
    connected_peers_start_string = "CPSS"
    chain_start_string = "CHAIN"
    transaction_start_string = "TR"

    @staticmethod
    def verify_peer_id(peer_id, peers):
        if peer_id in peers:
            return peers.index(peer_id)
        return False

    @staticmethod
    def custom_read(f):
        data = f.recv(100000).decode()
        return data
        chunks = []
        # bytes_recd = 0
        receiving = True
        while receiving:
            chunk = f.recv(2048)
            if not chunk:
                receiving = False
            chunks.append(chunk)
            # bytes_recd = bytes_recd + len(chunk)
        data = b''.join(chunks)
        return data.decode()

    @staticmethod
    def custom_read_old(f):
        #data = f.recv(1024).decode()
        fragments = []
        while True:
            chunk = f.recv(10000)
            if not chunk:
                break
            fragments.append(chunk)
        data = b''.join(fragments)
        print(data)
        return data.decode()

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
        peer_id = MyHelpers.peer_id_start_string + uuid.uuid4().hex[:6].upper().hex
        return peer_id

    @staticmethod
    def get_part_of_peers(connected_peers, convert_to_string=False):
        connected_peers_ = []
        if len(connected_peers) <= 10:
            for connected_peer in connected_peers:
                data = {
                    'peer_id': connected_peer['peer_id'],
                    'host': connected_peer['host'],
                    'port': connected_peer['port']
                }
                connected_peers_.append(data)
            if convert_to_string is True:
                return json.dumps(connected_peers_)

            return connected_peers_

        # randomly select a part of the list, containing 10 peers
        connected_peers_sublist = random.sample(connected_peers, 10)
        for connected_peer in connected_peers_sublist:
            data = {
                'peer_id': connected_peer['peer_id'],
                'host': connected_peer['host'],
                'port': connected_peer['port']
            }
            connected_peers_.append(data)
        if convert_to_string is True:
            return json.dumps(connected_peers_)
        return connected_peers_

    @staticmethod
    def get_peer_chain(cheesechain):
        chain_snapshot = cheesechain.get_chain()
        # convert the cheesechain object to dictionary, to be able to parse to json
        chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
        # again, convert the transactions in block from objects to dictionary
        for cheese_dict in chain_dictionary:
            cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]
        return json.dumps(chain_dictionary)

    @staticmethod
    def get_peer_open_transactions(cheesechain):
        transactions = cheesechain.get_open_transactions()
        transactions_dictionary = [tr.__dict__ for tr in transactions]
        return json.dumps(transactions_dictionary)
