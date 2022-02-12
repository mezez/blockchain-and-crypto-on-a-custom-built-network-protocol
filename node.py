from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin

from wallet import Wallet
from cheesechain import Cheesechain

app = Flask(__name__)
CORS(app)
# api = Api(app)
wallet = Wallet()
cheesechain = Cheesechain(wallet.public_key)

"""routes"""


@app.route('/', methods=['GET'])
def get_ui():
    return 'Home'


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
    chain_snapshot = cheesechain.get_chain()
    # convert the cheesechain object to dictionary, to be able to parse to json
    chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
    # again, convert the transactions in block from objects to dictionary
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
    transactions = cheesechain.get_open_transactions() # transactions object
    transactions_dictionary = [tr.__dict__ for tr in transactions]
    return jsonify(transactions_dictionary), 200


@app.route('/mine', methods=['GET'])
def mine():
    cheese = cheesechain.mine_cheese()  # cheese object
    if cheese is not None:
        cheese_dictionary = cheese.__dict__.copy()
        cheese_dictionary['transactions'] = [tr.__dict__ for tr in cheese_dictionary['transactions']]
        response = {
            'message': 'Block added successfully',
            'block': cheese_dictionary,
            'balance': cheesechain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'New block could not be added',
            'wallet_set_up': wallet.public_key is not None
        }
        return jsonify(response), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
