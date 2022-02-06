# initialize cheesechain list
import json
import sys
import hashlib
from collections import OrderedDict

from utils.hash_util import hash_cheese, hash_string_sha256
from cheese import Cheese
from transaction import Transaction

MINING_REWARD = 10  # CHEESECOIN

open_transactions = []
cheesechain = []

owner = 'Mez'
participants = {'Mez'}
VALID_HASH_CONDITION = '00'
CHEESECHAIN_FILE = 'cheesechain.txt'


def load_data():
    global cheesechain, open_transactions  # let python know that we are trying to use the global variables, not create new local ones
    try:
        with open(CHEESECHAIN_FILE, mode='r') as file:
            file_contents = file.readlines()

            cheesechain = json.loads(file_contents[0])  # first line is the cheesechain

            # the chain retrieved above contains transactions in a different format to how is was before saving
            # this can cause chain verification to fail. So it is formatted to it's original form
            # cheesechain = [
            #     {
            #         'parent_smell': cheese['parent_smell'],
            #         'sequence_number': cheese['sequence_number'],
            #         'transactions': [OrderedDict([
            #             ('sender', transaction['sender']),
            #             ('recipient', transaction['recipient']),
            #             ('amount', transaction['amount'])
            #         ]) for transaction in cheese['transactions']],
            #         'nonce': cheese['nonce']
            #     }
            #     for cheese in cheesechain]

            # alternative code with for loop
            formatted_cheesechain = []
            for cheese in cheesechain:
                # note: block content ordering does not matter here since they are ordered by keys in hashing function
                formatted_tx = [Transaction(transaction['sender'], transaction['recipient'], transaction['amount']) for transaction in cheese['transactions']]

                formatted_cheese = Cheese(cheese['sequence_number'], cheese['parent_smell'], formatted_tx, cheese['nonce'], cheese['timestamp'])

                formatted_cheesechain.append(formatted_cheese)
            cheesechain = formatted_cheesechain

            open_transactions = json.loads(file_contents[1])  # first line is the cheesechain
            formatted_transactions = []
            for transaction in open_transactions:
                formatted_transaction = [Transaction(transaction['sender'], transaction['recipient'], transaction['amount'])]
                formatted_transactions.append(formatted_transaction)
            open_transactions = formatted_transactions
    except IOError:
        print("Cheesechain data file not found. Initializing new chain...")
        # starting cheese for the cheesechain
        raclette_cheese = Cheese(0, '', [], 100, 0)
        cheesechain.append(raclette_cheese)


load_data()


def save_data():
    try:
        with open(CHEESECHAIN_FILE, mode='w') as file:
            # convert the cheesechain object into a dictionary that can be parsed to json
            # this also involves a nested conversion of the transactions list of objects into a list of dictionaries
            save_able_chain = [cheese.__dict__ for cheese in [Cheese(ch.sequence_number, ch.parent_smell, [tr.__dict__ for tr in ch.transactions], ch.nonce, ch.timestamp) for ch in cheesechain]]
            file.write(json.dumps(save_able_chain))
            file.write('\n')
            # convert the list of transactions object into a list of transactions dictionary to be able to parse to json
            save_able_tr = [tr.__dict__ for tr in open_transactions]
            file.write(json.dumps(save_able_tr))
    except IOError:
        print('Data could not be saved')


def valid_proof(transactions, parent_smell, nonce):
    # guess a new hash
    guess = (str([tr.to_ordered_dictionary() for tr in transactions]) + str(parent_smell) + str(nonce)).encode()
    guess_smell = hash_string_sha256(guess)
    print(guess_smell)
    # check if guess hash stars with 2 leading zeros
    return guess_smell[0:2] == VALID_HASH_CONDITION


def proof_of_work():
    last_cheese = cheesechain[-1]
    parent_smell = hash_cheese(last_cheese)
    nonce = 0
    _valid_proof = False
    while not _valid_proof:  # execute until valid proof is true
        _valid_proof = valid_proof(open_transactions, parent_smell, nonce)
        if not _valid_proof:
            nonce += 1
    return nonce


def get_balance(participant):
    """

    :param participant: a person involved in a transaction
    :return: a float cumulative cheesecoin balance of the participant
    """
    tx_sender = [[tx.amount for tx in cheese.transactions if tx.sender == participant] for cheese in
                 cheesechain]
    # get all the transaction amount sent by user, waiting to be mined in open transactions queue
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx.amount for tx in cheese.transactions if tx.recipient == participant] for cheese in
                    cheesechain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def get_last_cheese_chain_value():
    """

    :return: returns the last value of the current cheesechain
    """
    if len(cheesechain) < 1:
        return None
    return cheesechain[-1]


def verify_transaction(transaction):
    """

    :param transaction: a dictionary containing transaction details
    :return: confirm that sender has enough balance to carry out a transaction
    """
    sender_balance = get_balance(transaction.sender)
    if sender_balance >= transaction.amount:
        return True
    return False


def add_transaction(recipient, sender=owner, amount=1.0):
    """

    :param recipient: receiver of cheesecoin
    :param sender: sender of cheesechain
    :param amount: amount of cheesecoins sent in the transaction, default value 1.0
    :return: boolean
    """
    # transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    # replace with ordered dictionary

    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):  # confirm that there is enough money in sender's account
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_cheese():
    last_cheese = cheesechain[-1]  # last cheese in the chain

    parent_smell = hash_cheese(last_cheese)
    nonce = proof_of_work()

    # reward_transaction = {
    #     'sender': 'CHEESECHAIN REWARD SYSTEM',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }

    # use ordered dictionary instead
    # Rewards are only added if mining is successful
    reward_transaction = Transaction('CHEESECHAIN REWARD SYSTEM', owner, MINING_REWARD)

    # reward transactions will not appear in the global open transactions
    # if for some reason, the mining failed, so a copy is made
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    cheese = Cheese(len(cheesechain), parent_smell, copied_transactions, nonce)
    cheesechain.append(cheese)
    return True


def get_transaction_value():
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


def get_user_choice():
    """ Returns the input of the user (option selected)"""
    user_input = input("Your choice: ")
    return user_input


def print_cheesechain_elements():
    # output the cheesechain list to the console
    for cheese in cheesechain:
        print('outputting cheese')
        print(cheese)
    else:
        print("-" * 20)


def verify_chain():
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
        if not valid_proof(cheese.transactions[:-1], cheese.parent_smell,
                           cheese.nonce):  # select all parts of the list except the reward transaction
            print('Invalid proof of work - verify')
            print(index)
            print(cheese)
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

    # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid


waiting_for_input = True

# continuously mine/add data to the chain and print
while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction details")
    print("2: Mine a new cheese")
    print("3: Output the cheesechain cheeses")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, sender=owner, amount=amount):
            print('Transaction added')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2':
        if mine_cheese():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_cheesechain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == "q":
        waiting_for_input = False
        # continue
    else:
        print("Invalid input. Please pick a value from the list")
    if not verify_chain():
        print("invalid cheesechain")
        print_cheesechain_elements()
        break
    print('Remaining Balance for {}: {:6.2f}'.format('Mez', get_balance('Mez')))
else:
    print("User left")

print("done")
