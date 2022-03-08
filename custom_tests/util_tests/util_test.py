import time
import unittest

from cheese import Cheese
from utils import hash_util
from utils import utils
from utils import verification
from utils.verification import Verification


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
        if hash_cheese_type == None or cheese_type==None:
            self.fail("Either hash cheese or cheese object is None")
        self.assertNotEqual(hash_cheese_type, cheese_type)

    def test_convert_cheese_dictionary_to_object(self):
        #create a cheese as dictionary
        #pass it through the method
        #check if the result is an object then pass the test
        #or if the result is empty then fail the test

        cheese_dict = {"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 100, "timestamp": 0}
        sample_cheese = Cheese(0, '', [], 100, 0)
        cheese_type = type(sample_cheese)

        result = utils.GeneralUtils.convert_cheese_dictionary_to_object(cheese_dict)

        if result.sequence_number == "" :
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

        transaction_dict = {"sender": "CHEESECHAIN REWARD SYSTEM", "recipient": "30819f300d06092a86001", "amount": 10, "signature": "rewardtransactionsignature"}

    def test_valid_proof(self):

        sample_cheese = Cheese(1, "589aabe32e351af0b04d2c6d1d6e0c", [ {"sender": "CHEESECHAIN REWARD SYSTEM", "recipient": "30819f300d0609090203010001", "amount": 10, "signature": "rewardtransactionsignature"}], 6, time.time())
        valid_proof_object = Verification.valid_proof()