from flask import Flask, jsonify
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


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = cheesechain.get_chain()
    # convert the cheesechain object to dictionary, to be able to parse to json
    chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
    # again, convert the transactions in block from objects to dictionary
    for cheese_dict in chain_dictionary:
        cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]
    return jsonify(chain_dictionary), 200


@app.route('/mine', methods=['GET'])
def mine():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
