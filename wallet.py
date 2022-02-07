import binascii
import time

from Crypto.PublicKey import RSA
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
                print(public_key)
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
