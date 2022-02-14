from cheese import Cheese
from transaction import Transaction


class GeneralUtils:
    @staticmethod
    def convert_cheese_dictionary_to_object(cheese):
        formatted_tx = [
            Transaction(transaction['sender'], transaction['recipient'], transaction['signature'],
                        transaction['amount'])
            for transaction in cheese['transactions']]

        formatted_cheese = Cheese(cheese['sequence_number'], cheese['parent_smell'], formatted_tx,
                                  cheese['nonce'], cheese['timestamp'])

        return formatted_cheese

    @staticmethod
    def convert_transaction_object_to_dictionary(transactions):

        return [tr.__dict__ for tr in transactions]


