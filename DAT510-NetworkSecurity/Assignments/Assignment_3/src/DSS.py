#%%
'''
Author: Asahi Cantu Moreno
Descriptipn: DSS is a class for Digitas Signature Schema, implementing RSA Algorithm for message signature
'''
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Cryptodome import Random, PublicKey
from base64 import b64encode, b64decode

def newkeys(keysize):
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   private, public = key, key.publickey()
   return public, private

def extract_priv_key(priv_key):
    n = priv_key.n
    e = priv_key.e
    d = priv_key.d
    p = priv_key.p
    q = priv_key.q
    u = priv_key.u
    return (n, e, d, p, q, u)

def extract_pub_key(pub_key):
    n = pub_key.n
    e = pub_key.e
    return {'n':n,'e':e}

def create_pub_key(pub_key_dict):
    n = pub_key_dict['n']
    e = pub_key_dict['e']
    return RSA.RsaKey(n=n,e=e)

def rebuild_pub_key(components):
    n = components.n
    e = components.e
    d = components.d
    p = components.p
    q = components.q
    u = components.u
    return PublicKey.RsaKey(n=n, e=e, d=d, p=p, q=q, u=u)


def encrypt(message, pub_key):
   cipher = PKCS1_OAEP.new(pub_key)
   return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
   cipher = PKCS1_OAEP.new(priv_key)
   return cipher.decrypt(ciphertext)

# Authorization
def sign(message, priv_key):
    signer = PKCS1_v1_5.new(priv_key)
    digest = SHA512.new()
    digest.update(message)
    return signer.sign(digest)

#Authentication
def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA512.new()
    digest.update(message)
    verified = signer.verify(digest, signature)
    return verified
# %%
#Sign and send the message
def test():
    public, private = newkeys(1024)
    message = 'Hello'
    msg = message.encode('UTF-8')
    crypt = encrypt(msg,public)
    msg = decrypt(crypt,private)
    message = msg.decode('UTF-8')
    message
    pub_key, priv_key = newkeys(1024)
    message = 'This is my  hidden message'.encode('UTF-8')
    bit_file = b''
    with open("README.md",'rb') as f:
        while (byte := f.read(1)):
            bit_file+=byte
    signature = sign(bit_file,priv_key)     
    #signature = sign(message,priv_key) 
    #Receive and verify the message
    #verified = verify(message,signature,pub_key)
    verified = verify(bit_file,signature,pub_key)
# %%
