import time
import unittest

from cheese import Cheese
from utils import hash_util
from utils import utils
from utils import verification
from utils.verification import Verification
import transaction


class UtilTest(unittest.TestCase):

    def test_hash(self):
        hash_method = hash_util.hash_string_sha256
        string_to_hash = "jgjgjk".encode()
        result = hash_method(string_to_hash)
        self.assertNotEqual(string_to_hash, result, "Hssh successful")
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

    def test_convert_transaction_object_to_dictionary(self):
        # Need a transaction object
        # Need a transaction dict
        # compare both types
        # Also check if it has all the fields

        sample_transaction = transaction.Transaction("CHEESECHAIN REWARD SYSTEM", "30819f300d06092a86001",
                                                     "rewardtransactionsignature", 10)

        # {"sender": "CHEESECHAIN REWARD SYSTEM", "recipient": "30819f300d06092a86001", "amount": 10, "signature": "rewardtransactionsignature"}
        transaction_type = type(sample_transaction)

        print(transaction_type)
        result = utils.GeneralUtils.convert_transaction_object_to_dictionary(sample_transaction)
        result_type = type(result)
        if result['sender'] == "":
            self.fail("Sender can not be null")
        if result['recipient'] == "":
            self.fail("Recipient can not be null")
        if result['amount'] == "":
            self.fail("Amount can not be null")
        if result['signature'] == "":
            self.fail("Signature can not be null")

        self.assertNotEqual(result_type, None)
        self.assertEqual(result_type, transaction_type)

    def test_valid_proof(self):
        sample_cheese = Cheese(1, "589aabe32e398b6b8e3eab39ebdd3976b657dbdf8562251af0b04d2c6d1d6e0c", [
            {"sender": "CHEESECHAIN REWARD SYSTEM", "recipient": "30819f300d06092a818d6c99090203010001", "amount": 10,
             "signature": "rewardtransactionsignature"}], 6, time=time())
        result = Verification.valid_proof(sample_cheese.transactions, sample_cheese.parent_smell, sample_cheese.nonce)
        self.assertEqual(result[0:2], Verification.VALID_HASH_CONDITION)

    # def test_verify_chain(self):

    # get a valid cheeseChain object

    # pass it to Verification.verify_chain
    # result should be TRUE

    # pass an invalid cheeseChain object
    # the results should be FALSE

    # def test_verify_transactions(self):
    # # Ask Mez
    #
    # def test_verify_transaction(self):
    # #