import hashlib
import json

def hash_string_sha256(string):
    """

    :param string: input string to be hashed
    :return: sha256 hashed string of the input string
    """
    return hashlib.sha256(string).hexdigest()

def hash_cheese(cheese):
    """

    :param cheese: a single unit of the cheesechain
    :return: string hash value representing the cheese
    """
    hashable_cheese = cheese.__dict__.copy()
    #convert transaction objects to json serializable format instead of it's current object state
    hashable_cheese['transactions'] = [tr.to_ordered_dictionary() for tr in hashable_cheese['transactions']]
    return hash_string_sha256(json.dumps(hashable_cheese, sort_keys=True).encode())
    # order the keys of the cheese and generate hash,
    # this ensures consistency the output hash generated,
    # preventing issues with reording of keys in the dictionary