# initialize cheesechain list
import json
import sys

from utils.hash_util import hash_cheese
from cheese import Cheese
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10  # CHEESECOIN
VALID_HASH_CONDITION = '00'
CHEESECHAIN_FILE = 'cheesechain.txt'


class Cheesechain:
    def __init__(self, hosting_node_id):
        # starting cheese for the cheesechain
        raclette_cheese = Cheese(0, '', [], 100, 0)
        self.my_cheesechain = [raclette_cheese]
        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def load_data(self):
        try:
            with open(CHEESECHAIN_FILE, mode='r') as file:
                file_contents = file.readlines()

                cheesechain = json.loads(file_contents[0])  # first line is the cheesechain

                formatted_cheesechain = []
                for cheese in cheesechain:
                    # note: block content ordering does not matter here since they are ordered by keys in hashing function
                    formatted_tx = [Transaction(transaction['sender'], transaction['recipient'], transaction['amount'])
                                    for transaction in cheese['transactions']]

                    formatted_cheese = Cheese(cheese['sequence_number'], cheese['parent_smell'], formatted_tx,
                                              cheese['nonce'], cheese['timestamp'])

                    formatted_cheesechain.append(formatted_cheese)
                self.my_cheesechain = formatted_cheesechain

                open_transactions = json.loads(file_contents[1])  # first line is the cheesechain
                formatted_transactions = []
                for transaction in open_transactions:
                    formatted_transaction = [
                        Transaction(transaction['sender'], transaction['recipient'], transaction['amount'])]
                    formatted_transactions.append(formatted_transaction)
                self.open_transactions = formatted_transactions
        except IOError:
            print("Cheesechain data file not found. Initializing new chain...")

    def save_data(self):
        try:
            with open(CHEESECHAIN_FILE, mode='w') as file:
                # convert the cheesechain object into a dictionary that can be parsed to json
                # this also involves a nested conversion of the transactions list of objects into a list of dictionaries
                save_able_chain = [cheese.__dict__ for cheese in [
                    Cheese(ch.sequence_number, ch.parent_smell, [tr.__dict__ for tr in ch.transactions], ch.nonce,
                           ch.timestamp) for ch in self.my_cheesechain]]
                file.write(json.dumps(save_able_chain))
                file.write('\n')
                # convert the list of transactions object into a list of transactions dictionary to be able to parse to json
                save_able_tr = [tr.__dict__ for tr in self.open_transactions]
                file.write(json.dumps(save_able_tr))
        except IOError:
            print('Data could not be saved')

    def proof_of_work(self):
        last_cheese = self.my_cheesechain[-1]
        parent_smell = hash_cheese(last_cheese)
        nonce = 0
        _valid_proof = False
        while not _valid_proof:  # execute until valid proof is true
            verifier = Verification()
            _valid_proof = verifier.valid_proof(self.open_transactions, parent_smell, nonce)
            if not _valid_proof:
                nonce += 1
        return nonce

    def get_balance(self):
        """

        :param participant: a person involved in a transaction
        :return: a float cumulative cheesecoin balance of the participant
        """
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in cheese.transactions if tx.sender == participant] for cheese in
                     self.my_cheesechain]
        # get all the transaction amount sent by user, waiting to be mined in open transactions queue
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        for tx in tx_sender:
            if len(tx) > 0:
                amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in cheese.transactions if tx.recipient == participant] for cheese in
                        self.my_cheesechain]
        amount_received = 0
        for tx in tx_recipient:
            if len(tx) > 0:
                amount_received += tx[0]
        return amount_received - amount_sent

    def get_last_cheese_chain_value(self):
        """

        :return: returns the last value of the current cheesechain
        """
        if len(self.my_cheesechain) < 1:
            return None
        return self.my_cheesechain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        """

        :param recipient: receiver of cheesecoin
        :param sender: sender of cheesechain
        :param amount: amount of cheesecoins sent in the transaction, default value 1.0
        :return: boolean
        """
        # transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
        # replace with ordered dictionary

        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction,
                                       self.get_balance):  # confirm that there is enough money in sender's account
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_cheese(self):
        last_cheese = self.my_cheesechain[-1]  # last cheese in the chain

        parent_smell = hash_cheese(last_cheese)
        nonce = self.proof_of_work()

        # reward_transaction = {
        #     'sender': 'CHEESECHAIN REWARD SYSTEM',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }

        # use ordered dictionary instead
        # Rewards are only added if mining is successful
        reward_transaction = Transaction('CHEESECHAIN REWARD SYSTEM', self.hosting_node, MINING_REWARD)

        # reward transactions will not appear in the global open transactions
        # if for some reason, the mining failed, so a copy is made
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        cheese = Cheese(len(self.my_cheesechain), parent_smell, copied_transactions, nonce)
        self.my_cheesechain.append(cheese)
        # reset open transactions and save
        self.open_transactions = []
        self.save_data()
        return True
