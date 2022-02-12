import sys

from flask import Flask, jsonify, request, send_from_directory
# from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import ast
import socket

from wallet import Wallet
from cheesechain import Cheesechain
from cheese_network.peer import Peer
from cheese_network.my_helpers import MyHelpers

app = Flask(__name__)
CORS(app)
# api = Api(app)
wallet = Wallet()
cheesechain = Cheesechain(wallet.public_key)

peer_object = None
peer_chains = []
peer_open_transactions = []

"""routes"""


@app.route('/', methods=['GET'])
def get_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global cheesechain
        cheesechain = Cheesechain(wallet.public_key)
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
        cheesechain = Cheesechain(wallet.public_key)
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
    # connect to a network tracker if not connected already
    global peer_object
    if peer_object is None:
        peer_object = Peer()
        # print(peer_object.__dict__)
        print("My Peer")
    if peer_object is not None:
        print("PEER_OBJ")
        connected_peers = peer_object.request_connected_peers()
        connected_peers = connected_peers.replace(MyHelpers.connected_peers_start_string, '')
        connected_peers = ast.literal_eval(connected_peers)

        # loop through the peers and request chains from them if the peer id doesn't match yours
        count = 0
        for connected_peer in connected_peers:
            connected_peer_id = connected_peer['peer_id']
            connected_peer_host = connected_peer['host']
            connected_peer_port = connected_peer['port']
            connected_peer_socket = connected_peer['socket']
            # connect to peer
            print("Connecting to peer with details: ")
            print("Host: ", connected_peer_host)
            print("port: ", connected_peer_port)
            s = socket.create_connection((connected_peer_host, connected_peer_host))
            print("connected to: ", s)

            # request chain
            peer_chain = peer_object.request_chain(connected_peer_socket)
            peer_chain = peer_chain.replace(MyHelpers.chain_start_string, '')
            peer_chain = ast.literal_eval(peer_chain)
            peer_chains.append(peer_chain)

            # request open transactions
            peer_tr = peer_object.request_open_transactions(connected_peer_socket)
            peer_tr = peer_tr.replace(MyHelpers.transaction_start_string, '')
            peer_tr = ast.literal_eval(peer_tr)
            peer_open_transactions.append(peer_tr)


            count += 1

        sys.exit("bye for now")
        # compare their chains among themselves and with yours, pick the longest chain
        # update your chain if it is outdated, notify others with different chains if so
        # return the up-to-date chain
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
    transactions = cheesechain.get_open_transactions()  # transactions object
    transactions_dictionary = [tr.__dict__ for tr in transactions]
    return jsonify(transactions_dictionary), 200


@app.route('/mine', methods=['POST'])
def mine():
    cheese = cheesechain.mine_cheese()  # cheese object
    if cheese is not None:
        cheese_dictionary = cheese.__dict__.copy()
        cheese_dictionary['transactions'] = [tr.__dict__ for tr in cheese_dictionary['transactions']]
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


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5005)
    args = parser.parse_args()
    port = args.port
    # run with python node.py -p [port]
    # default port will be 5005 if not specified
    app.run(host='0.0.0.0', port=port)
