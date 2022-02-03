# initialize cheesechain list
import sys

MINING_REWARD = 10 #CHEESECOIN

open_transactions = []
cheesechain = []
raclette_cheese = {'previous_smell': '', 'sequence_number': 0, 'transactions': []}
cheesechain.append(raclette_cheese)
owner = 'Mez'
participants = {'Mez'}


def hash_cheese(cheese):
    return '-'.join([str(cheese[key]) for key in cheese])  # list comprehension


def get_balance(participant):
    #get all the transaction amount sent by user, already in the blockchain
    tx_sender = [[tx['amount'] for tx in cheese['transactions'] if tx['sender'] == participant] for cheese in cheesechain]
    # get all the transaction amount sent by user, waiting to be mined in open transactions queue
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in cheese['transactions'] if tx['recipient'] == participant] for cheese in cheesechain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def get_last_cheese_chain_value():
    """ returns the last value of the current cheesechain
    """
    if len(cheesechain) < 1:
        return None
    return cheesechain[-1]


def verify_transaction(transaction):
    """confirm that sender has enough balance to carry out a transaction"""
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    return False


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a transaction

    :arguments
    sender: sender of cheesechain
    recipient: receiver of cheesecoin
    amount: amount of cheesecoins sent in the transaction, default value 1.0
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    if verify_transaction(transaction): # confirm that there is enough money in sender's account
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_cheese():
    last_cheese = cheesechain[-1]  # last cheese in the chain

    #method one :for loop
    # parent_smell = ''
    # for key in last_cheese:
    #     value = last_cheese[key]
    #     parent_smell = parent_smell + str(value)

    #method two :list comprehension
    parent_smell = hash_cheese(last_cheese)

    reward_transaction = {
        'sender': 'CHEESECHAIN REWARD SYSTEM',
        'recipient': owner,
        'amount': MINING_REWARD,
    }

    # ensure that rewards are only added if mining is successfuly
    # reward transactions will not appear in the global open transactions if mining is unsuccessful
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    open_transactions.append(reward_transaction)
    cheese = {'previous_smell': parent_smell, 'sequence_number': len(cheesechain), 'transactions': copied_transactions}
    cheesechain.append(cheese)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float value"""
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


# proof of work
def verify_chain():
    is_valid = True
    for (index, cheese) in enumerate(cheesechain): # enumerate returns a tuple with the index of an element and the element itself
        if index == 0:
            #first element
            continue
        if cheese['previous_smell'] != hash_cheese(cheesechain[index - 1]):
            """comparing the previous hash of the current cheese with a recalculated hash of the cheese preceding this cheese. 
            if the previous cheese was manipulated..."""
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
    print('Remaining Balance for {}: {:6.2f}'.format('Mez',get_balance('Mez')))
else:
    print("User left")

print("done")
