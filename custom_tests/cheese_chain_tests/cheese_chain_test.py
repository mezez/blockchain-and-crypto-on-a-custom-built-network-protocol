import unittest

from cheese import Cheese
from cheesechain import Cheesechain
from transaction import Transaction
from collections import OrderedDict
from wallet import Wallet

class CheeseChainTest(unittest.TestCase):
    #transaction.py
    def test_to_ordered_dictionary(self):
        recipient = "30819f300d06092a818d6c99090203010001"
        sender = "CHEESECHAIN REWARD SYSTEM"
        signature = "rewardtransactionsignature"
        amount = 10
        sample_transaction = Transaction(sender, recipient, signature, amount)
        result = Transaction.to_ordered_dictionary(sample_transaction)
        self.assertEqual(type(result), OrderedDict)

    #wallet.py
    def test_create_keys(self):
        #does not return anything
        return True

    def test_save_keys(self):
        sample_wallet = Wallet(1)
        sample_wallet.create_keys()
        result = sample_wallet.save_keys()
        self.assertEqual(type(result), bool)

    def test_load_keys(self):
        sample_wallet = Wallet(1)
        sample_wallet.create_keys()
        result = sample_wallet.load_keys()
        self.assertEqual(type(result), bool)

    def test_generate_keys(self):
        sample_wallet = Wallet(1)
        sample_wallet.create_keys()
        result = sample_wallet.generate_keys()
        self.assertEqual(type(result), tuple)

    def test_sign_transaction(self):
        sample_wallet = Wallet(1)
        sample_wallet.create_keys()
        recipient = "30819f300d06092a818d6c99090203010001"
        sender = "CHEESECHAIN REWARD SYSTEM"
        amount = 10
        result = sample_wallet.sign_transaction(sender, recipient, amount)
        self.assertEqual(type(result), str)

    def test_verify_signature(self):
        recipient = "30819f300d06092a818d6c99090203010001"
        sender = "CHEESECHAIN REWARD SYSTEM"
        amount = 10
        sample_wallet = Wallet(1)
        sample_wallet.create_keys()
        sample_signature = sample_wallet.sign_transaction(sender, recipient, amount)

        sample_transaction = Transaction(sender, recipient, sample_signature, amount)
        result = sample_wallet.verify_signature(sample_transaction)
        self.assertEqual(type(result), bool)

    def test_make_string_length_even(self):
        return True
    #CheeseChain
    def test_get_chain(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 1
        sample_cheese_chain = Cheesechain(public_key, node_id)
        result = sample_cheese_chain.get_chain()
        self.assertEqual(type(result), type(sample_cheese_chain))

    def test_get_open_transactions(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 1
        sample_cheese_chain = Cheesechain(public_key, node_id)
        result = sample_cheese_chain.get_open_transactions()
        self.assertEqual(type(result), dict)

    def test_load_data(self):
        #Ask Mez - returns nothing
        return True

    def test_save_data(self):
        # Ask Mez - returns nothing
        return True

    def test_overwrite_data(self):
        # Ask Mez - returns nothing
        #Cheesechain.overwrite_data()
        return True

    def test_proof_of_work(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 1
        sample_cheese_chain = Cheesechain(public_key, node_id)
        nonce = sample_cheese_chain.proof_of_work()
        if nonce == None:
            self.assertEqual(nonce, None)
        self.assertEqual(type(nonce), int)

    def test_get_balance(self):
        balance = Cheesechain.get_balance('30819f300d06092a864886f70d010101050003818d0030818902818100d847a586a3521e8967ffe9d494bf9b070b1752c98c2bc251231a29c3546678a357f2d18563756aa4ea2be80aa8e9f9f6760cfa8c8322471f2a40f8b3ddcc20603ecf041a6b4ebb9027cc1e88982ecd727407181beeaeb971b23de7d9a635dc046e67a3e62a79edeaeb4a419f633cb63244076429b21d78dfe5e213b166610bd90203010001')
        if balance == None:
            self.assertEqual(balance, None)
        self.assertEqual(type(balance), int)


    def test_get_last_cheese_chain_value(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 1
        sample_cheese_chain = Cheesechain(public_key, node_id)
        result = sample_cheese_chain.get_last_cheese_chain_value()
        if result == None:
            self.assertEqual(result, None)
        self.assertEqual(type(result), Cheese)

    def test_transaction_exists_in_cheesechain(self):
        recipient = "30819f300d06092a818d6c99090203010001"
        sender = "CHEESECHAIN REWARD SYSTEM"
        signature = "rewardtransactionsignature"
        amount = 10
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 1
        sample_chain = Cheesechain(public_key, node_id)
        chain_snapshot = sample_chain.get_chain()
        chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
        # again, convert the transactions in cheese from objects to dictionary
        for cheese_dict in chain_dictionary:
            cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]

        result = sample_chain.transaction_exists_in_cheesechain(chain_dictionary, recipient, sender, signature, amount)
        self.assertEqual(type(result), bool)


    def test_remove_already_added_transactions(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 1
        sample_chain = Cheesechain(public_key, node_id)
        chain_snapshot = sample_chain.get_chain()
        chain_dictionary = [cheese.__dict__.copy() for cheese in chain_snapshot]
        # again, convert the transactions in cheese from objects to dictionary
        for cheese_dict in chain_dictionary:
            cheese_dict['transactions'] = [tr.__dict__ for tr in cheese_dict['transactions']]
        result = sample_chain.remove_already_added_transactions(chain_dictionary)
        self.assertEqual(result, True)

    def test_add_transaction(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 0
        chain_instance = Cheesechain(public_key, node_id)
        recipient = "30819f300d06092a818d6c99090203010001"
        sender = "CHEESECHAIN REWARD SYSTEM"
        signature = "rewardtransactionsignature"
        amount = 10
        result = Cheesechain.add_transaction(chain_instance, recipient, sender, signature, amount)
        self.assertEqual(type(result), bool)

    def test_mine_cheese(self):
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 0
        chain_instance = Cheesechain(public_key, node_id) #pass public_key node_id
        result = Cheesechain.mine_cheese(chain_instance)

        if result==None:
            self.assertEqual(result, None)
        self.assertEqual(type(result), Cheese)

    def test_add_cheese(self):
        sample_cheese = Cheese(1, "589aabe32e398b6b8e3eab39ebdd3976b657dbdf8562251af0b04d2c6d1d6e0c", [{"sender": "CHEESECHAIN REWARD SYSTEM", "recipient": "30819f300d06092a818d6c99090203010001", "amount": 10, "signature": "rewardtransactionsignature"}], 6, 1647429844.220142)

        sample_cheese['transactions'] = [tr.__dict__ for tr in sample_cheese['transactions']]
        public_key = "30819f300d06092a864886f70d010101050003818d0030818902818100d7dcb93709aff291b10c3634276aa53f7912749e269f9da7e906d07b1de590f0486a52bc0ba60cc9ad2a6126324f021a670aec0b5da311859f875749122becd63a4053ef366764816c0337b61e9dc7b4e009dd97dc41cc66861c488552a70c26b02a10076ae26a5f17e67f4b8e0078d6b4a73df0f713cf77267c34bb94564c310203010001"
        node_id = 0
        cheese_chain_instance = Cheesechain(public_key, node_id)
        result = cheese_chain_instance.add_cheese(sample_cheese)
        self.assertEqual(type(result), bool)

    #node.py
    def test_get_ui(self):
        return  True

    def test_create_keys(self):
        return True

    def test_load_keys(self):
        return True

    def test_get_balance(self):
        return True

    def test_get_chain(self):
        return True

    def test_add_transaction(self):
        return True

    def test_get_open_transactions(self):
        return True

    def test_mine(self):
        return True

    def test_get_connected_pears(self):
        return True

    def test_get_peer_chain(self):
        return True

    def test_get_peer_transactions(self):
        return True

    def test_add_cheese_from_remote_peer(self):
        return True

    def test_broadcast_cheese_to_peers(self):
        return True

    def test_broadcast_tr_to_peers(self):
        return True

    def test_disconnect_from_peer(self):
        return True


    def test_(self):
        return True

    def test_(self):
        return True

