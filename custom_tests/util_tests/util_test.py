import time
import unittest

from cheese import Cheese
from utils import hash_util
from utils import utils
from utils.verification import Verification
from transaction import Transaction


class UtilTest(unittest.TestCase):

    def test_hash(self):
        hash_method = hash_util.hash_string_sha256
        string_to_hash = "jgjgjk".encode()
        result = hash_method(string_to_hash)
        self.assertNotEqual(string_to_hash, result, "Hash successful")
        # assert string_to_hash != result

    def test_hash_cheese(self):
        raclette_cheese = Cheese(0, '', [], 100, 0)
        cheese_type = type(raclette_cheese)
        result = hash_util.hash_cheese(raclette_cheese)
        hash_cheese_type = type(result)
        print(cheese_type)
        if hash_cheese_type == None or cheese_type == None:
            self.fail("Either hash cheese or cheese object is None")
        self.assertNotEqual(hash_cheese_type, cheese_type)

    def test_convert_cheese_dictionary_to_object(self):
        # create a cheese as dictionary
        # pass it through the method
        # check if the result is an object then pass the test
        # or if the result is empty then fail the test

        cheese_dict = {"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 100, "timestamp": 0}
        sample_cheese = Cheese(0, '', [], 100, 0)
        cheese_type = type(sample_cheese)

        result = utils.GeneralUtils.convert_cheese_dictionary_to_object(cheese_dict)

        if result.sequence_number == "":
            self.fail("Sequence number is empty")
        if result.transactions == "":
            self.fail("Transactions field is empty")
        if result.nonce == "":
            self.fail("Nonce is empty")
        if result.parent_smell == "" and result.sequence_number != 0:
            self.fail("Parent Smell is empty")

        result_type = type(result)
        print(cheese_type)
        self.assertEqual(result_type, cheese_type)

    def test_valid_proof(self):
        sample_cheese = Cheese(1, "589aabe32e398b6b8e3eab39ebdd3976b657dbdf8562251af0b04d2c6d1d6e0c", [
            {"sender": "CHEESECHAIN REWARD SYSTEM", "recipient": "30819f300d06092a818d6c99090203010001", "amount": 10,
             "signature": "rewardtransactionsignature"}], 6, 1647429844.220142)
        formattted_transactions = self.convert_dict_transaction_to_object_transaction(sample_cheese.transactions)
        result = Verification.valid_proof(formattted_transactions, sample_cheese.parent_smell, sample_cheese.nonce)
        result_type = type(result)
        self.assertEqual(result_type, bool)

    def test_verify_chain(self):
        valid_cheesechain = [
            {"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 100, "timestamp": 0},
            {"sequence_number": 1, "parent_smell": "589aabe32e398b6b8e3eab39ebdd3976b657dbdf8562251af0b04d2c6d1d6e0c",
             "transactions": [{"sender": "CHEESECHAIN REWARD SYSTEM",
                               "recipient": "30819f300d06092a864886f70d010101050003818d0030818902818100d847a586a3521e8967ffe9d494bf9b070b1752c98c2bc251231a29c3546678a357f2d18563756aa4ea2be80aa8e9f9f6760cfa8c8322471f2a40f8b3ddcc20603ecf041a6b4ebb9027cc1e88982ecd727407181beeaeb971b23de7d9a635dc046e67a3e62a79edeaeb4a419f633cb63244076429b21d78dfe5e213b166610bd90203010001",
                               "amount": 0.5, "signature": "rewardtransactionsignature"}], "nonce": 6,
             "timestamp": 1647429844.220142}]
        formatted_cheesechain1 = self.convert_dict_cheesechain_to_object_cheesechain(valid_cheesechain)

        result1 = Verification.verify_chain(formatted_cheesechain1)
        self.assertEqual(result1, True)

        invalid_cheesechain = [
            {"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 10, "timestamp": 0},
            {"sequence_number": 2, "parent_smell": "589aabe32e398b6b8e3eab39ebdd3976b657dbdf8562251af0b04d2c6d1d6e0c",
             "transactions": [{"sender": "CHEESECHAIN REWARD SYSTEM",
                               "recipient": "30819f300d06092a864886f70d010101050003818d0030818902818100d847a586a3521e8967ffe9d494bf9b070b1752c98c2bc251231a29c3546678a357f2d18563756aa4ea2be80aa8e9f9f6760cfa8c8322471f2a40f8b3ddcc20603ecf041a6b4ebb9027cc1e88982ecd727407181beeaeb971b23de7d9a635dc046e67a3e62a79edeaeb4a419f633cb63244076429b21d78dfe5e213b166610bd90203010001",
                               "amount": 0.5, "signature": "rewardtransactionsignature"}], "nonce": 6,
             "timestamp": 1647429844.220142}]
        formatted_cheesechain2 = self.convert_dict_cheesechain_to_object_cheesechain(invalid_cheesechain)
        result2 = Verification.verify_chain(formatted_cheesechain2)
        self.assertNotEqual(result2, True)

    def convert_dict_cheesechain_to_object_cheesechain(self, cheesechain):
        formatted_cheesechain = []
        for cheese in cheesechain:
            # note: block content ordering does not matter here since they are ordered by keys in hashing function
            formatted_tx = [
                Transaction(transaction['sender'], transaction['recipient'], transaction['signature'],
                            transaction['amount'])
                for transaction in cheese['transactions']]

            formatted_cheese = Cheese(cheese['sequence_number'], cheese['parent_smell'], formatted_tx,
                                      cheese['nonce'], cheese['timestamp'])

            formatted_cheesechain.append(formatted_cheese)
        return formatted_cheesechain

    def convert_dict_transaction_to_object_transaction(self, transactions):
        formatted_tx = [
            Transaction(transaction['sender'], transaction['recipient'], transaction['signature'],
                        transaction['amount'])
            for transaction in transactions
        ]
        return formatted_tx


if __name__ == '__main__':
    unittest.main()
