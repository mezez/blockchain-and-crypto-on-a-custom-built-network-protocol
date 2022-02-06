from utils.hash_util import hash_cheese, hash_string_sha256


class Verification:
    VALID_HASH_CONDITION = '00'

    def valid_proof(self, transactions, parent_smell, nonce):
        # guess a new hash
        guess = (str([tr.to_ordered_dictionary() for tr in transactions]) + str(parent_smell) + str(nonce)).encode()
        guess_smell = hash_string_sha256(guess)
        print(guess_smell)
        # check if guess hash stars with 2 leading zeros
        return guess_smell[0:2] == self.VALID_HASH_CONDITION

    def verify_chain(self, cheesechain):
        """confirm validity of the current cheesechain. returns true for a valid chain and false for an invalid one"""
        for (index, cheese) in enumerate(
                cheesechain):  # enumerate returns a tuple with the index of an element and the element itself
            if index == 0:
                # first element
                continue
            """comparing the previous hash/smell of the current cheese with a recalculated hash of the cheese preceding this cheese. 
                        if the previous cheese was manipulated..."""
            if cheese.parent_smell != hash_cheese(cheesechain[index - 1]):
                return False
            """confirm that the the previous hash/smell in the of a cheese in the cheese chain was generated using the accepted algorithm of this system.
                So we will be able to generate a hash that meets the defined valid hash condition with the previous hash, nonce and open transactions provided
            """
            if not self.valid_proof(cheese.transactions[:-1], cheese.parent_smell,
                                    cheese.nonce):  # select all parts of the list except the reward transaction
                print('Invalid proof of work - verify')
                print(index)
                print(cheese)
                return False

        return True

    def verify_transactions(self, open_transactions, get_balance):
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])

        # is_valid = True
        # for tx in open_transactions:
        #     if verify_transaction(tx):
        #         is_valid = True
        #     else:
        #         is_valid = False
        # return is_valid

    def verify_transaction(self, transaction, get_balance):
        """

        :param get_balance: pointer to a get_balance function
        :param transaction: a dictionary containing transaction details
        :return: confirm that sender has enough balance to carry out a transaction
        """
        sender_balance = get_balance()
        if sender_balance >= transaction.amount:
            return True
        return False
