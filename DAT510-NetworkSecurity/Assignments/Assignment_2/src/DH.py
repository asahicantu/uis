'''
@Author: Asahi Cantu Moreno
@Student id: 253964
@Description: Diphie-Hellman key exchange implementation
'''
import argparse
import logging
import hashlib
import base64
from Cryptodome.Cipher import AES
from Cryptodome import Random

logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

class DH(object):
    '''
    DH is a the contraction for Diphie-Hellman key exchange algoithm implementation
    It works by implementing cryptographic shared key interchange to later on send an shared key withi which any message can be
    decrypted by using a unique generated private key.

    Cryptographic explanation:
        Algorithm uses  multiplicative group of integers modulo p, where p is prime, and g is a primitive root modulo p. 
        These two values are chosen in this way to ensure that the resulting shared secret 
        can take on any value from 1 to p–1.

        1. Users A and B  publicly agree to use a modulus p = 23 and base g = 5 ( primitive root modulo 23).
        2. A chooses a private key  a = 4, then sends to B [ A = g^a mod p  = 5^4 mod 23 = 4|
        3. B chooses a secret integer b = 3, then sends to A [ B = g^b mod p  = 5^3 mod 23 = 10 ]
        4. A computes s = B^a mod p [ 104 mod 23 = 18 ]
        5. B computes s =  A^b mod p [ s = 43 mod 23 = 18 ]
        6. A and B now share a secret (the number 18).
        7. A and B have arrived at the same values because under mod p,
    '''
    @staticmethod
    def log_message(message):
        logger.info(message)
        
    def __init__(self, public_key1, public_key2, private_key):
        DH.log_message("Initializing Diffie–Hellman key exchange...")
        DH.log_message(f'\tPublic key1: {public_key1}')
        DH.log_message(f'\tPublic key2: {public_key2}')
        DH.log_message(f'\tPrivate key: {private_key}')
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.shared_key = None
        self.full_key = None
    
    @staticmethod
    def _pad(s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
        
    def create_shared_key(self):
        DH.log_message(f'Creating Shared key...')
        self.shared_key = (self.public_key1 ** self.private_key) % self.public_key2
        DH.log_message(f'\t Shared key created {self.shared_key}')
        return self.shared_key
    
    def create_full_key(self, shared_key):
        DH.log_message('Creating full key...')
        self.full_key  = (shared_key ** self.private_key) % self.public_key2
        DH.log_message(f'\tFull Key created {self.full_key}!')
        self.full_key = hashlib.sha256(str(self.full_key).encode()).digest()
        DH.log_message(f'\tAfter SHA Key created {self.full_key}!')
        return self.full_key

    
    def encrypt(self, message):
        DH.log_message('Encrypting message with AES...')
        DH.log_message(f'\t[{message}]')
        message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        DH.log_message(f'\tInitialization Vector created {iv}!')
        cipher = AES.new(self.full_key, AES.MODE_CBC, iv)
        enc =  base64.b64encode(iv + cipher.encrypt(message.encode()))
        DH.log_message(f'\tMessage Encrypted!')
        DH.log_message(f'\t[{enc}]')
        return enc
    
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        message = ''
        DH.log_message('Decrypting message...')
        DH.log_message(f'\t[{enc}]')
        iv = enc[:AES.block_size]
        DH.log_message(f'\tInitialization Vector created {iv}!')
        cipher = AES.new(self.full_key, AES.MODE_CBC, iv)
        message = self._unpad(cipher.decrypt(enc[AES.block_size:]))
        message = message.decode('utf-8')
        DH.log_message(f'Message Decrypted! {message}')
        return message