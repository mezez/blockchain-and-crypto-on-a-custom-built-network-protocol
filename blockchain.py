# initialize cheesechain list
import json
import sys
import hashlib
from collections import OrderedDict

MINING_REWARD = 10  # CHEESECOIN

open_transactions = []
cheesechain = []
raclette_cheese = {'previous_smell': '', 'sequence_number': 0, 'transactions': [], 'nonce': 100}
cheesechain.append(raclette_cheese)
owner = 'Mez'
participants = {'Mez'}
VALID_HASH_CONDITION = '00'


def valid_proof(transactions, parent_smell, nonce):
    # guess a new hash
    guess = (str(transactions) + str(parent_smell) + str(nonce)).encode()
    guess_smell = hashlib.sha256(guess).hexdigest()
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


def hash_cheese(cheese):
    """

    :param cheese: a single unit of the cheesechain
    :return: string hash value representing the cheese
    """
    return hashlib.sha256(json.dumps(cheese, sort_keys=True).encode()).hexdigest()
    # order the keys of the cheese and generate hash,
    # this ensures consistency the output hash generated,
    # preventing issues with reording of keys in the dictionary


def get_balance(participant):
    """

    :param participant: a person involved in a transaction
    :return: a float cumulative cheesecoin balance of the participant
    """
    tx_sender = [[tx['amount'] for tx in cheese['transactions'] if tx['sender'] == participant] for cheese in
                 cheesechain]
    # get all the transaction amount sent by user, waiting to be mined in open transactions queue
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in cheese['transactions'] if tx['recipient'] == participant] for cheese in
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
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    return False


def add_transaction(recipient, sender=owner, amount=1.0):
    """

    :param recipient: receiver of cheesecoin
    :param sender: sender of cheesechain
    :param amount: amount of cheesecoins sent in the transaction, default value 1.0
    :return: boolean
    """
    #transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    #replace with ordered dictionary

    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):  # confirm that there is enough money in sender's account
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
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

    #use ordered dictionary instead
    reward_transaction = OrderedDict([
        ('sender', 'CHEESECHAIN REWARD SYSTEM'), ('recipient', owner), ('amount', MINING_REWARD)
    ])

    # ensure that rewards are only added if mining is successful
    # reward transactions will not appear in the global open transactions if mining is unsuccessful
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    open_transactions.append(reward_transaction)
    cheese = {'previous_smell': parent_smell, 'sequence_number': len(cheesechain), 'transactions': copied_transactions, 'nonce': nonce}
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
        if cheese['previous_smell'] != hash_cheese(cheesechain[index - 1]):
            return False
        """confirm that the the previous hash/smell in the of a cheese in the cheese chain was generated using the accepted algorithm of this system.
            So we will be able to generate a hash that meets the defined valid hash condition with the previous hash, nonce and open transactions provided
        """
        if not valid_proof(cheese['transactions'][:-1], cheese['previous_smell'], cheese['nonce']): #select all parts of the list except the reward transaction
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
    print("h: Manipulate the chain")
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
    elif user_choice == '3':
        print_cheesechain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(cheesechain) >= 1:
            cheesechain[0] = [
                {
                    'previous_smell': '',
                    'sequence_number': 0,
                    ' transactions': [{'sender': 'Sara', 'recipient': 'Randika', 'Amount': 22.24}]
                }
            ]
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
