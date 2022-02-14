# initialize cheesechain list
import json
import sys
import ast
import socket

from utils.hash_util import hash_cheese
from cheese import Cheese
from transaction import Transaction
from wallet import Wallet
from utils.verification import Verification


class Cheesechain:
    CHEESECHAIN_FILE = 'cheesechain.txt'
    CHEESECHAIN_REWARD_SYSTEM = 'CHEESECHAIN REWARD SYSTEM'
    REWARD_TRANSACTION_SIGNATURE = 'rewardtransactionsignature'
    MINING_REWARD = 10  # CHEESECOIN

    #def __init__(self, public_key, node_id, peer_object=None, connected_peers=None):
    def __init__(self, public_key, node_id):
        # starting cheese for the cheesechain
        raclette_cheese = Cheese(0, '', [], 100, 0)
        self.__my_cheesechain = [raclette_cheese]
        self.__open_transactions = []
        self.node_id = node_id
        self.load_data()
        self.public_key = public_key
        # self.peer_object = peer_object
        # self.connected_peers = connected_peers


    # @property
    # def chain(self):
    #    return self.__my_cheesechain[:]

    # @chain.setter
    # def chain(self, val):
    #    self.__my_cheesechain = val

    def get_chain(self):
        return self.__my_cheesechain

    def get_open_transactions(self):
        return self.__open_transactions

    def load_data(self):
        try:
            # with open(Cheesechain.CHEESECHAIN_FILE, mode='r') as file:

            # each file will correspond to the node that created it
            with open('cheesechain-{}.txt'.format(self.node_id), mode='r') as file:
                file_contents = file.readlines()

                cheesechain = json.loads(file_contents[0])  # first line is the cheesechain

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
                self.__my_cheesechain = formatted_cheesechain

                open_transactions = json.loads(file_contents[1])  # first line is the cheesechain
                formatted_transactions = []
                for transaction in open_transactions:
                    formatted_transaction = Transaction(transaction['sender'], transaction['recipient'], transaction['signature'],transaction['amount'])
                    formatted_transactions.append(formatted_transaction)
                self.__open_transactions = formatted_transactions
        except IOError:
            print("Cheesechain data file not found. Initializing new chain...")

    def save_data(self):
        try:
            # with open(Cheesechain.CHEESECHAIN_FILE, mode='w') as file:
            with open('cheesechain-{}.txt'.format(self.node_id), mode='w') as file:
                # convert the cheesechain object into a dictionary that can be parsed to json
                # this also involves a nested conversion of the transactions list of objects into a list of dictionaries
                save_able_chain = [cheese.__dict__ for cheese in [
                    Cheese(ch.sequence_number, ch.parent_smell, [tr.__dict__ for tr in ch.transactions], ch.nonce,
                           ch.timestamp) for ch in self.__my_cheesechain]]
                file.write(json.dumps(save_able_chain))
                file.write('\n')
                # convert the list of transactions object into a list of transactions dictionary to be able to parse to json
                save_able_tr = [tr.__dict__ for tr in self.__open_transactions]
                file.write(json.dumps(save_able_tr))
        except IOError:
            print('Data could not be saved')

    def proof_of_work(self):
        last_cheese = self.__my_cheesechain[-1]
        parent_smell = hash_cheese(last_cheese)
        nonce = 0
        _valid_proof = False
        while not _valid_proof:  # execute until valid proof is true
            _valid_proof = Verification.valid_proof(self.__open_transactions, parent_smell, nonce)
            if not _valid_proof:
                nonce += 1
        return nonce

    def get_balance(self, sender=None):
        """

        :param sender: the creator of transaction
        :param participant: a person involved in a transaction
        :return: a float cumulative cheesecoin balance of the participant
        """
        if sender is None:
            if self.public_key is None:
                # no public key available
                return None
            participant = self.public_key
        else:
            participant = sender

        tx_sender = [[tx.amount for tx in cheese.transactions if tx.sender == participant] for cheese in
                     self.__my_cheesechain]
        # get all the transaction amount sent by user, waiting to be mined in open transactions queue
        print('Get balance')
        print(self.__my_cheesechain)
        print(self.__open_transactions)
        # sys.exit()
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        for tx in tx_sender:
            if len(tx) > 0:
                amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in cheese.transactions if tx.recipient == participant] for cheese in
                        self.__my_cheesechain]
        amount_received = 0
        for tx in tx_recipient:
            if len(tx) > 0:
                amount_received += tx[0]
        return amount_received - amount_sent

    def get_last_cheese_chain_value(self):
        """

        :return: returns the last value of the current cheesechain
        """
        if len(self.__my_cheesechain) < 1:
            return None
        return self.__my_cheesechain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """

        :param node_port: port on which web server is listening
        :param recipient: receiver of cheesecoin
        :param sender: sender of cheesechain
        :param signature: signed string of sender showing authenticity
        :param amount: amount of cheesecoins sent in the transaction, default value 1.0
        :return: boolean
        """
        # transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
        # replace with ordered dictionary
        if self.public_key is None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)

        # confirm that there is enough money in sender's account and transaction has a valid signature
        if Verification.verify_transaction(transaction,
                                           self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            # self.broadcast_added_transaction(recipient, sender, signature, amount)
            return True
        return False

    def mine_cheese(self):
        """
        Create a new cheese and add open transactions to it
        :return: True for success, False otherwise
        """
        if self.public_key is None:
            return None
        last_cheese = self.__my_cheesechain[-1]  # last cheese in the chain

        parent_smell = hash_cheese(last_cheese)
        nonce = self.proof_of_work()

        # reward_transaction = {
        #     'sender': 'CHEESECHAIN REWARD SYSTEM',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }

        # use ordered dictionary instead
        # Rewards are only added if mining is successful
        reward_transaction = Transaction(Cheesechain.CHEESECHAIN_REWARD_SYSTEM, self.public_key,
                                         Cheesechain.REWARD_TRANSACTION_SIGNATURE, Cheesechain.MINING_REWARD)

        # reward transactions will not appear in the global open transactions
        # if for some reason, the mining failed, so a copy is made
        copied_transactions = self.__open_transactions[:]
        # verify signatures for all transactions in this cheese (excluding reward transactions)
        for tr in copied_transactions:
            if not Wallet.verify_signature(tr):
                return None
        copied_transactions.append(reward_transaction)

        cheese = Cheese(len(self.__my_cheesechain), parent_smell, copied_transactions, nonce)
        self.get_chain().append(cheese)
        # reset open transactions and save
        self.__open_transactions = []
        self.save_data()
        return cheese

    def add_cheese(self, cheese):
        # validate and add
        transactions = [Transaction(tr['sender'], tr['recipient'], tr['signature'], tr['amount']) for tr in cheese['transactions']]

        # confirm proof of work
        is_valid = Verification.valid_proof(transactions, cheese['previous_smell'], cheese['nonce'])

        # confirm if the hash of our last cheese matches the last cheese stored in the incoming cheese
        hashes_match = hash_cheese(self.get_chain()[-1]) == cheese['previous_smell']

        if not is_valid or not hashes_match:
            return False
        converted_cheese = Cheese(cheese['sequence_number'], cheese['previous_smell'], transactions, cheese['nonce'], cheese['timestamp'])
        self.__my_cheesechain.append(converted_cheese)
        self.save_data()
        return True
