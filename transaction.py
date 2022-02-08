from collections import OrderedDict

from utils.printable import Printable


class Transaction(Printable):
    """
    Transaction to be added to a cheese in the cheesechain

    Attributes
    :sender: sender of cheesecoins
    :recipient: receiver of cheesecoins
    :signature: transaction signature
    :amount: quantity of cheesecoins sent
    """
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dictionary(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
