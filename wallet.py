import binascii
import sys
import time

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random

time.clock = time.time


class Wallet:
    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key.strip()
        self.public_key = public_key.strip()

    def save_keys(self):
        # save keys to file
        if self.private_key is not None and self.private_key is not None:
            try:
                with open('wallet-{}.txt'.format(self.node_id), mode='w') as wallet_file:
                    wallet_file.write(self.public_key)
                    wallet_file.write('\n')
                    wallet_file.write(self.private_key)
                return True
            except(IOError, IndexError):
                print('Keys could not be saved to file')
                return False

    def load_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode='r') as wallet_file:
                keys = wallet_file.readlines()
                # public_key = keys[:-1] # skip the \n character ??
                public_key = keys[0]
                private_key = keys[1]

                self.public_key = public_key.strip()
                self.private_key = private_key.strip()
            return True
        except(IOError, IndexError):
            print('Keys could not be loaded')
            return False

    def generate_keys(self):
        # public and private key in binary form
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()

        # string version
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode(),
                binascii.hexlify(public_key.exportKey(format='DER')).decode())

    def sign_transaction(self, sender, recipient, amount):
        """
        create a signature to be used for every new transaction
        :param sender:
        :param recipient:
        :param amount:
        :return:
        """
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key.strip())))
        payload_hash = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(payload_hash)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_signature(transaction):
        """
        Confirm authenticity of transaction signature
        :param transaction: transaction containing signature
        :return: True of verified or False otherwise
        """
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender.strip()))
        verifier = PKCS1_v1_5.new(public_key)
        payload_hash = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(payload_hash, binascii.unhexlify(transaction.signature))

    @staticmethod
    def make_string_length_even(key):
        print(key)
        if len(key) % 2 == 0:
            return key
        else:
            key = key + "0"
            print(key)
            return key
