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
    return hash_string_sha256(json.dumps(cheese, sort_keys=True).encode())
    # order the keys of the cheese and generate hash,
    # this ensures consistency the output hash generated,
    # preventing issues with reording of keys in the dictionary