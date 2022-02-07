from time import time

from utils.printable import Printable


class Cheese(Printable):
    def __init__(self, sequence_number, parent_smell, transactions, nonce, time=time()):
        self.sequence_number = sequence_number
        self.parent_smell = parent_smell
        self.transactions = transactions
        self.nonce = nonce
        self.timestamp = time
