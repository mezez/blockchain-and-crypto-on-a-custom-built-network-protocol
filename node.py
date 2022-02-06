import sys
from uuid import uuid4

from cheesechain import Cheesechain
from verification import Verification

class Node:
    def __init__(self):
        #self.id = str(uuid4())  # parse string to make value json serializable
        self.id = 'Mez'  # parse string to make value json serializable
        self.cheesechain = Cheesechain(self.id)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose")
            print("1: Add a new transaction details")
            print("2: Mine a new cheese")
            print("3: Output the cheesechain cheeses")
            print("4: Check transaction validity")
            print("q: Quit")
            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.cheesechain.add_transaction(recipient, self.id, amount=amount):
                    print('Transaction added')
                else:
                    print('Transaction failed')
                print(self.cheesechain.open_transactions)
            elif user_choice == '2':
                self.cheesechain.mine_cheese()
            elif user_choice == '3':
                self.print_cheesechain_elements()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(self.cheesechain.open_transactions, self.cheesechain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == "q":
                waiting_for_input = False
                # continue
            else:
                print("Invalid input. Please pick a value from the list")
            verifier = Verification()
            if not verifier.verify_chain(self.cheesechain.my_cheesechain):
                print("invalid cheesechain")
                self.print_cheesechain_elements()
                break
            print('Remaining Balance for {}: {:6.2f}'.format(self.id, self.cheesechain.get_balance()))
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
        for cheese in self.cheesechain.my_cheesechain:
            print('outputting cheese')
            print(cheese)
        else:
            print("-" * 20)


node = Node()
node.listen_for_input()