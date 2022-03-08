import json
import sys

from flask import Flask, jsonify, request, send_from_directory
# from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import ast
import socket

from wallet import Wallet
from transaction import Transaction
from cheese import Cheese
from cheesechain import Cheesechain
from utils.verification import Verification
from utils.utils import GeneralUtils
from cheese_network.peer import Peer
from cheese_network.cheese_protocol import CheeseProtocol
from cheese_network.my_helpers import MyHelpers

app = Flask(__name__)
CORS(app)
# api = Api(app)

peer_object = None
peer_chains = []
peer_open_transactions = []
connected_peers = None
just_connecting = True
chain_dictionary = []

TRACKER_URL = "81.250.246.39"

exists = False

"""routes"""


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global cheesechain
        cheesechain = Cheesechain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': cheesechain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': "Keys could not be saved"
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global cheesechain
        cheesechain = Cheesechain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': cheesechain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': "Keys could not be loaded"
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = cheesechain.get_balance()
    if balance is not None:
        response = {
            'message': "Success",
            'balance': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'message': "Balance could not be loaded",
            'wallet_set_up': wallet.public_key is not None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    # TODO WRAP IN TRY BLOCK AFTER TESTS
    # connect to a network tracker if not connected already
    global peer_object
    global connected_peers
    global just_connecting
    global chain_dictionary
    global peer_chains
    if peer_object is None:
        #connection_url = TRACKER_URL+":"+port
        peer_object = Peer(port)
        # print(peer_object.__dict__)
    if peer_object is not None:
        if connected_peers is None:
            connected_peers = get_connected_pears(peer_object)

        # loop through the peers and request chains from them if the peer id doesn't match yours
        if just_connecting:
            print("just connecting")
            count = 0
            peer_chains = []
            for connected_peer in connected_peers:
                # TODO WRAP IN TRY BLOCK AFTER TESTS
                try:
                    connected_peer_id = connected_peer['peer_id']
                    # don't connect to yourself
                    if connected_peer_id != peer_object.peer_id:
                        connected_peer_host = connected_peer['host']
                        connected_peer_port = connected_peer['port']
                        # connected_peer_socket = connected_peer['socket']

                        # connect to peer
                        print("Connecting to peer with details: ")
                        print("Host: ", connected_peer_host)
                        print("port: ", connected_peer_port)
                        s = socket.create_connection((connected_peer_host, connected_peer_port))
                        print("connected to: ", s)

                        # request chain
                        # port here is the port on which the node app is running
                        # necessary for differentiating wallets and chains of the different nodes
                        peer_chain = get_peer_chain(peer_object, s)
                        peer_chains.append(peer_chain)

                        # request open transactions
                        # port here is the port on which the node app is running
                        # peer_tr = get_peer_transactions(peer_object, s)
                        # peer_open_transactions.append(peer_tr)
                        # TODO SEND DISCONNECTION MESSAGE
                        s.close()  # close connection after retrieving chain

                        # disconnect from peer

                except:
                    # could not connect to peer, move to next
                    pass
                count += 1

            # sys.exit("bye for now")
            # compare their chains among themselves and with yours, pick the longest chain
            chain_snapshot = cheesechain.get_chain()
            chain_dictionary = []
            chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
            # again, convert the transactions in cheese from objects to dictionary
            for cheese_dict in chain_dictionary:
                cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]

            print("length of peer chains", len(peer_chains))
            for ch in peer_chains:
                # validate chain
                formatted_cheesechain = []
                for cheese in ch:
                    cheese = GeneralUtils.convert_cheese_dictionary_to_object(cheese)
                    formatted_cheesechain.append(cheese)
                verified = Verification.verify_chain(formatted_cheesechain)
                if verified:
                    print('verified')
                    print(len(ch))
                    print(len(chain_dictionary))
                    if len(ch) > len(chain_dictionary):
                        # chain_dictionary = []
                        chain_dictionary = ch
                        my_open_tr = cheesechain.get_open_transactions()
                        save_able_tr = GeneralUtils.convert_transaction_object_to_dictionary(my_open_tr)
                        cheesechain.overwrite_data(ch, save_able_tr)
                        # cheesechain.load_data()
                else:
                    continue
            # update your chain if it is outdated, notify others with different chains if so
            # return the up-to-date chain
            # just_connecting = False

        # update transactions
        # for peer_transactions in peer_open_transactions:
        #     for incoming_transaction in peer_transactions:
        #         global exists
        #         exists = False
        #         cheesechain.load_data()
        #         my_open_tr = cheesechain.get_open_transactions()
        #         for open_transaction in my_open_tr:
        #             if open_transaction.sender == incoming_transaction['sender'] and open_transaction.recipient == \
        #                     incoming_transaction['recipient'] and open_transaction.amount == incoming_transaction[
        #                 'amount'] \
        #                     and open_transaction.signature == incoming_transaction['signature']:
        #                 exists = True
        #         if not exists:
        #             cheesechain.add_transaction(incoming_transaction['recipient'], incoming_transaction['sender'],
        #                                         incoming_transaction['signature'], incoming_transaction['amount'])
    cheesechain.load_data()
    chain_snapshot = cheesechain.get_chain()
    # convert the cheesechain object to dictionary, to be able to parse to json
    chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
    # again, convert the transactions in cheese from objects to dictionary
    for cheese_dict in chain_dictionary:
        cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]
    return jsonify(chain_dictionary), 200


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key is None:
        response = {
            'message': 'Wallet has not been setup'
        }
        return jsonify(response), 400
    # data = request.get_data()
    data = request.get_json()
    if not data:
        response = {
            'message': 'transaction data is required'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in data for field in required_fields):
        response = {
            'message': 'recipient and amount are required'
        }
        return jsonify(response), 400
    recipient = data['recipient']
    amount = data['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)

    transaction_added = cheesechain.add_transaction(recipient, wallet.public_key, signature, amount)

    if transaction_added:
        # inform other peers gotten from tracker of new transaction verified and added to open transactions
        # each peer will verify and also try to add the transaction to their open transactions and try to broadcast
        # to their own peers as well
        broadcast_tr_to_peers(recipient, wallet.public_key, signature, amount)

        # send response
        response = {
            'message': 'Transaction added successfully',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature,
            },
            'balance': cheesechain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Transaction could not be added'
        }
        return jsonify(response), 500


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    # TODO WRAP IN TRY BLOCK AFTER TESTS
    # connect to a network tracker if not connected already
    global peer_object
    global connected_peers
    global chain_dictionary
    global just_connecting
    global peer_chains
    global peer_open_transactions
    if peer_object is None:
        just_connecting = True
        peer_object = Peer(port)
        # print(peer_object.__dict__)
    if peer_object is not None:
        if connected_peers is None:
            connected_peers = get_connected_pears(peer_object)

        if just_connecting:
            peer_chains = []
            peer_open_transactions = []
            # loop through the peers and request chains from them if the peer id doesn't match yours
            count = 0
            for connected_peer in connected_peers:
                # TODO WRAP IN TRY BLOCK AFTER TESTS
                try:
                    connected_peer_id = connected_peer['peer_id']
                    # don't connect to yourself
                    if connected_peer_id != peer_object.peer_id:
                        connected_peer_host = connected_peer['host']
                        connected_peer_port = connected_peer['port']
                        # connected_peer_socket = connected_peer['socket']

                        # connect to peer
                        print("Connecting to peer with details: ")
                        print("Host: ", connected_peer_host)
                        print("port: ", connected_peer_port)
                        s = socket.create_connection((connected_peer_host, connected_peer_port))
                        print("connected to: ", s)

                        # request chain
                        # port here is the port on which the node app is running
                        # necessary for differentiating wallets and chains of the different nodes
                        peer_chain = get_peer_chain(peer_object, s)
                        peer_chains.append(peer_chain)

                        # request open transactions
                        # port here is the port on which the node app is running
                        peer_tr = get_peer_transactions(peer_object, s)
                        peer_open_transactions.append(peer_tr)
                        # TODO SEND DISCONNECTION MESSAGE
                        s.close()  # close connection after retrieving chain

                        # disconnect from peer
                except:
                    pass
                count += 1

            # sys.exit("bye for now")
            # compare their TR among themselves and with yours, verify and add valid ones to your sys
            # update your tr if it is outdated, notify others with different tr if so
            chain_snapshot = cheesechain.get_chain()
            chain_dictionary = []
            chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
            # again, convert the transactions in cheese from objects to dictionary
            for cheese_dict in chain_dictionary:
                cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]

            for ch in peer_chains:
                # validate chain
                formatted_cheesechain = []
                for cheese in ch:
                    cheese = GeneralUtils.convert_cheese_dictionary_to_object(cheese)
                    formatted_cheesechain.append(cheese)
                verified = Verification.verify_chain(formatted_cheesechain)
                if verified:
                    print('verified')
                    print(len(ch))
                    print(len(chain_dictionary))
                    if len(ch) > len(chain_dictionary):
                        chain_dictionary = ch
                        my_open_tr = cheesechain.get_open_transactions()
                        save_able_tr = GeneralUtils.convert_transaction_object_to_dictionary(my_open_tr)
                        cheesechain.overwrite_data(chain_dictionary, save_able_tr)
                else:
                    continue
            # just_connecting = False
    # update transactions
    print('open transactions')
    print(peer_open_transactions)
    for peer_transactions in peer_open_transactions:
        for incoming_transaction in peer_transactions:
            global exists
            exists = False
            cheesechain.load_data()
            my_open_tr = cheesechain.get_open_transactions()
            for open_transaction in my_open_tr:
                if open_transaction.sender == incoming_transaction['sender'] and open_transaction.recipient == \
                        incoming_transaction['recipient'] and open_transaction.amount == incoming_transaction['amount']\
                        and open_transaction.signature == incoming_transaction['signature']:
                    exists = True
                if exists:
                    break
            if not exists:
                cheesechain.add_transaction(incoming_transaction['recipient'], incoming_transaction['sender'],
                                            incoming_transaction['signature'], incoming_transaction['amount'])

    # for peer_transactions in peer_open_transactions:
    #     for tr in peer_transactions:
    #         cheesechain.add_transaction(tr['recipient'], tr['sender'], tr['signature'], tr['amount'])
    cheesechain.load_data()
    transactions = cheesechain.get_open_transactions()  # transactions object
    transactions_dictionary = [tr.__dict__ for tr in transactions]
    return jsonify(transactions_dictionary), 200


@app.route('/mine', methods=['POST'])
def mine():
    cheese = cheesechain.mine_cheese()  # cheese object
    if cheese is not None:
        cheese_dictionary = cheese.__dict__.copy()
        cheese_dictionary['transactions'] = [tr.__dict__ for tr in cheese_dictionary['transactions']]

        # broadcast cheese
        broadcast_cheese_to_peers(cheese_dictionary)
        response = {
            'message': 'Cheese added successfully',
            'cheese': cheese_dictionary,
            'balance': cheesechain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'New cheese could not be added',
            'wallet_set_up': wallet.public_key is not None
        }
        return jsonify(response), 500


def get_connected_pears(peer_object_):
    my_connected_peers = peer_object_.request_connected_peers()
    my_connected_peers = my_connected_peers.replace(CheeseProtocol.GETPEERSRESP, '')
    my_connected_peers = ast.literal_eval(my_connected_peers)
    return my_connected_peers


def get_peer_chain(peer_object_, connected_peer_socket):
    peer_chain = peer_object_.request_chain(connected_peer_socket)
    peer_chain = peer_chain.replace(CheeseProtocol.GETCHAINRESP, '')
    peer_chain = ast.literal_eval(peer_chain)
    return peer_chain


def get_peer_transactions(peer_object_, connected_peer_socket):
    peer_tr = peer_object_.request_open_transactions(connected_peer_socket)
    peer_tr = peer_tr.replace(CheeseProtocol.GETOPENTRANSACTIONSRESP, '')
    peer_tr = ast.literal_eval(peer_tr)
    return peer_tr


def add_cheese_from_remote_peer(cheese):
    # confirm that the sequence number of this cheese is exactly greater than that of the receiving peer's
    # latest sequence number by 1, otherwise, the receiving peer is missing some blocks
    # or is already ahead of this cheese
    if cheese['index'] == cheesechain.get_chain()[-1].sequence_number + 1:

        cheese_added = cheesechain.add_cheese(cheese)

        if cheese_added:
            # broadcast to your connected peers received from tracker
            # broadcast_cheese_to_peers(cheese)
            pass
    elif cheese['index'] > cheesechain.get_chain()[-1].sequence_number:
        pass
    else:
        # incoming index is smaller than our last block index
        # TODO the broadcasting block is backwards and should be informed
        pass


def add_transaction_from_remote_peer(tr):
    recipient = tr['recipient']
    sender = tr['sender']
    amount = tr['amount']
    signature = tr['signature']
    transaction_added = cheesechain.add_transaction(recipient, sender, signature, amount)

    if transaction_added:
        # broadcast to your connected peers received from tracker
        # broadcast_tr_to_peers(recipient, signature, amount)
        pass


def broadcast_cheese_to_peers(cheese):
    # connect to a network tracker if not connected already
    # TODO WRAP IN TRY BLOCK AFTER TESTS
    # try: except: continue # continue on exception
    global peer_object
    global connected_peers
    if peer_object is None:
        peer_object = Peer(port)
        # print(peer_object.__dict__)
    if peer_object is not None:
        if connected_peers is None:
            connected_peers = get_connected_pears(peer_object)

        # loop through the peers and broadcast added transaction
        count = 0
        for connected_peer in connected_peers:
            #  WRAP IN TRY BLOCK AFTER TESTS
            try:
                connected_peer_id = connected_peer['peer_id']
                # prevent broadcast to self
                if connected_peer_id != peer_object.peer_id:
                    connected_peer_host = connected_peer['host']
                    connected_peer_port = connected_peer['port']
                    # connected_peer_socket = connected_peer['socket']
                    # connect to peer
                    print("Connecting to peer with details: ")
                    print("Host: ", connected_peer_host)
                    print("port: ", connected_peer_port)
                    s = socket.create_connection((connected_peer_host, connected_peer_port))
                    print("connected to: ", s)

                    #  send cheese and disconnect once acknowledged
                    peer_object.share_cheese(cheese, s, peer_object)
            except:
                # connection failed, move to next peer
                pass
            count += 1


def broadcast_tr_to_peers(recipient, sender, signature, amount):
    # connect to a network tracker if not connected already
    # TODO WRAP IN TRY BLOCK AFTER TESTS
    # try: except: continue # continue on exception
    global peer_object
    global connected_peers
    if peer_object is None:
        peer_object = Peer(port)
        # print(peer_object.__dict__)
    if peer_object is not None:
        if connected_peers is None:
            connected_peers = get_connected_pears(peer_object)

        # loop through the peers and broadcast added transaction
        count = 0
        for connected_peer in connected_peers:
            # TODO WRAP IN TRY BLOCK AFTER TESTS
            try:
                connected_peer_id = connected_peer['peer_id']
                # TODO prevent broadcast to self
                if connected_peer_id != peer_object.peer_id:
                    connected_peer_host = connected_peer['host']
                    connected_peer_port = connected_peer['port']
                    # connected_peer_socket = connected_peer['socket']
                    # connect to peer
                    print("Connecting to peer with details: ")
                    print("Host: ", connected_peer_host)
                    print("port: ", connected_peer_port)
                    s = socket.create_connection((connected_peer_host, connected_peer_port))
                    print("connected to: ", s)

                    #  send transaction and disconnect once acknowledged
                    tr = {'recipient': recipient, 'sender': sender, 'signature': signature, 'amount': amount}
                    peer_object.share_added_transaction(tr, s, peer_object)
            except:
                # connection failed, move to next peer
                pass
            count += 1


def disconnect_from_peer(peer_object, connected_peer_socket):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5005)
    args = parser.parse_args()
    port = args.port
    print("server:" + str(port))
    # run with python node.py -p [port]
    # default port will be 5005 if not specified

    wallet = Wallet(port)
    cheesechain = Cheesechain(wallet.public_key, port)
    # peer_object = Peer(port)

    app.run(host='0.0.0.0', port=port)
