import binascii
import time

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random

time.clock = time.time


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        # save keys to file
        if self.private_key is not None and self.private_key is not None:
            try:
                with open('wallet.txt', mode='w') as wallet_file:
                    wallet_file.write(self.public_key)
                    wallet_file.write('\n')
                    wallet_file.write(self.private_key)
            except(IOError, IndexError):
                print('Keys could not be saved to file')

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as wallet_file:
                keys = wallet_file.readlines()
                # public_key = keys[:-1] # skip the \n character ??
                public_key = keys[0]
                private_key = keys[1]

                self.public_key = public_key
                self.private_key = private_key
        except(IOError, IndexError):
            print('Keys could not be loaded')

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
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
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
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        payload_hash = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(payload_hash, binascii.unhexlify(transaction.signature))