import sys

from cheesechain import Cheesechain
from utils.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self):
        # self.id = str(uuid4())  # parse string to make value json serializable
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.cheesechain = Cheesechain(self.wallet.public_key)
        # self.cheesechain = None

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1: Add a new transaction details")
            print("2: Mine a new cheese")
            print("3: Output the cheesechain cheeses")
            print("4: Check transaction validity")
            print("5: Create wallet")
            print("6: Load wallet")
            print("7: Save keys")
            print("q: Quit")
            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.cheesechain.add_transaction(recipient, self.wallet.public_key, amount=amount):
                    print('Transaction added')
                else:
                    print('Transaction failed')
                print(self.cheesechain.get_open_transactions())
            elif user_choice == '2':
                if not self.cheesechain.mine_cheese():
                    print("Mining failed. Please confirm that you have a wallet")
            elif user_choice == '3':
                self.print_cheesechain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.cheesechain.get_open_transactions(),
                                                    self.cheesechain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == '5':
                # create a public key and then a blockchain
                self.wallet.create_keys()
                self.cheesechain = Cheesechain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.cheesechain = Cheesechain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == "q":
                waiting_for_input = False
                # continue
            else:
                print("Invalid input. Please pick a value from the list")
            if not Verification.verify_chain(self.cheesechain.get_chain()):
                print("invalid cheesechain")
                self.print_cheesechain_elements()
                break
            print('Remaining Balance for {}: {:6.2f}'.format(self.wallet.public_key, self.cheesechain.get_balance()))
        else:
            print("User left")

        print("done")

    def get_transaction_value(self):
        """

        :return: Returns the input of the user (a new transaction amount) as a float value
        """
        # random_string is used in this function scope
        try:
            transaction_recipient = input("Enter the recipient of transaction: ")
            transaction_amount = float(input("Enter the transaction amount: "))
            return (transaction_recipient, transaction_amount)
        except:
            print("Invalid amount!")
            sys.exit()

    def get_user_choice(self):
        """ Returns the input of the user (option selected)"""
        user_input = input("Your choice: ")
        return user_input

    def print_cheesechain_elements(self):
        # output the cheesechain list to the console
        for cheese in self.cheesechain.get_chain():
            print('outputting cheese')
            print(cheese)
        else:
            print("-" * 20)


# only execute this block when the file is run directly and not when it is imported
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
