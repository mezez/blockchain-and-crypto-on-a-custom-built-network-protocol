import unittest

import cheese
import cheesechain
from cheesechain import Cheesechain



class CheeseChainTest(unittest.TestCase):
    #transaction.py
    def test_to_ordered_dictionary(self):
        #Pass transaction details
        #Check if it returns ordered dictionary of transactions
        return  True
    #wallet.py
    def test_create_keys(self):
        #does not return anything
        return True

    def test_save_keys(self):
        #Check if the wallet has public and private keys
        #Check if the method returns True or False(boolean)
        return True

    def test_load_keys(self):
        #
        #Check if the value returned is boolean
        return True

    def test_generate_keys(self):
        return True

    def test_sign_transaction(self):
        #check if it returns value
        return True

    def test_verify_signature(self):
        return True

    def test_make_string_length_even(self):
        return True
    #CheeseChain
    def test_get_chain(self):
        return True

    def test_get_open_transactions(self):
        return True

    def test_load_data(self):
        #Ask Mez
        return True

    def test_save_data(self):
        return True

    def test_overwrite_data(self):
        cheesechain.Cheesechain.overwrite_data()
        return True

    def test_proof_of_work(self):
        nonce = cheesechain.Cheesechain.proof_of_work()
        if nonce == None:
            self.assertEqual(nonce, None)
        self.assertEqual(type(nonce), int)

    def test_get_balance(self):
        balance = cheesechain.get_balance('30819f300d06092a864886f70d010101050003818d0030818902818100d847a586a3521e8967ffe9d494bf9b070b1752c98c2bc251231a29c3546678a357f2d18563756aa4ea2be80aa8e9f9f6760cfa8c8322471f2a40f8b3ddcc20603ecf041a6b4ebb9027cc1e88982ecd727407181beeaeb971b23de7d9a635dc046e67a3e62a79edeaeb4a419f633cb63244076429b21d78dfe5e213b166610bd90203010001')
        if balance == None:
            self.assertEqual(balance, None)
        self.assertEqual(type(balance), int)


    def test_get_last_cheese_chain_value(self):
        return True

    def test_transaction_exists_in_cheesechain(self):
        return True

    def test_remove_already_added_transactions(self):
        return True

    def test_add_transaction(self):
        return True

    def test_mine_cheese(self):
        chain_instance = cheesechain.Cheesechain() #pass public_key node_id
        result = chain_instance.mine_cheese(chain_instance)
        if result==None:
            self.assertEqual(result, None)
        self.assertEqual(result, cheese.Cheese)

    def test_add_cheese(self):
        result = cheesechain.Cheesechain.add_cheese()
        self.assertEqual(type(result), bool)



