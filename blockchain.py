# initialize cheesechain list
import sys

open_transactions = []
cheesechain = []
raclette_cheese = {'previous_smell': '', 'sequence_number': 0, 'transactions': []}
cheesechain.append(raclette_cheese)
owner = 'Mez'


def hash_cheese(cheese):
    return '-'.join([str(cheese[key]) for key in cheese])  # list comprehension


def get_last_cheese_chain_value():
    """ returns the last value of the current cheesechain
    """
    if len(cheesechain) < 1:
        return None
    return cheesechain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a transaction

    :arguments
    sender: sender of cheesechain
    recipient: receiver of cheesecoin
    amount: amount of cheesecoins sent in the transaction, default value 1.0
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    open_transactions.append(transaction)


def mine_cheese():
    last_cheese = cheesechain[-1]  # last cheese in the chain

    #method one :for loop
    # parent_smell = ''
    # for key in last_cheese:
    #     value = last_cheese[key]
    #     parent_smell = parent_smell + str(value)

    #method two :list comprehension
    parent_smell = hash_cheese(last_cheese)

    cheese = {'previous_smell': parent_smell, 'sequence_number': len(cheesechain), 'transactions': open_transactions}
    cheesechain.append(cheese)


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



waiting_for_input = True

# continuously mine/add data to the chain and print
while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction details")
    print("2: Mine a new cheese")
    print("3: Output the cheesechain cheeses")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, sender=owner, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_cheese()
    elif user_choice == '3':
        print_cheesechain_elements()
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
else:
    print("User left")

print("done")
