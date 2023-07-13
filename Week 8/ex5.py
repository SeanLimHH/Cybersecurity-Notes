#---------------------------
# The context of this week's lab is to learn how the cryptographic hash
# algorithm works and its protocol.
#   
# The emphasis is on RSA as well.
# This exercise is to use the proper libraries to encrypt data and decrypt, with
# signing of it to ensure data integrity.
#---------------------------
from ex2 import *

def generate_RSA(bits = 1024):
    keyPair = RSA.generate(bits)
    return keyPair

def encrypt_RSA(publicKeyFileName, message):
    with open(publicKeyFileName, 'rb') as publicKeyFile:
        # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        key = RSA.import_key(publicKeyFile.read())
        # https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)
    return ciphertext
    
def decrypt_RSA(privateKeyFileName, ciphertext):
    with open(privateKeyFileName, 'rb') as privateKeyFile:
        # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        key = RSA.import_key(privateKeyFile.read())
        # https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def sign_data(privateKeyFileName, data): #* Signs the data
    with open(privateKeyFileName, 'rb') as privateKeyFile:
        # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        key = RSA.import_key(privateKeyFile.read())
        # https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html
    hashedValue = SHA256.new()
    hashedValue.update(data)
    signature = PKCS1_PSS.new(key).sign(hashedValue)
    return signature

def verify_sign(publicKeyFileName, signature, data): #* Signs the data
    with open(publicKeyFileName, 'rb') as publicKeyFile:
        # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        key = RSA.import_key(publicKeyFile.read())
        # https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html
    
    hashedValue = SHA256.new()
    hashedValue.update(data)
    verificationResult = PKCS1_PSS.new(key).verify(hashedValue, signature)
    return verificationResult

if __name__ == '__main__':
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA256
    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.Signature import PKCS1_PSS
    publicKeyFileName = 'public_key_file.PEM'
    privateKeyFileName = 'private_key_file.PEM'
    messageFileName = 'mydata.txt'
    
    with open(messageFileName, 'rb') as messageFile:
        message = messageFile.read()
    
    keyPair = generate_RSA()
    with open(publicKeyFileName, 'wb') as publicKeyFile:
        # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        publicKeyFile.write(keyPair.publickey().export_key('PEM'))
    
    with open(privateKeyFileName, 'wb') as privateKeyFile:
        # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
        privateKeyFile.write(keyPair.export_key('PEM'))
        
    ciphertext = encrypt_RSA(publicKeyFileName, message)
    print('\nciphertext: ', ciphertext)
    decrypted = decrypt_RSA(privateKeyFileName, ciphertext)
    print('\ndecrypted: ', decrypted)
    
    signature = sign_data(privateKeyFileName, message)
    print('\nsignature: ', signature)
    
    verificationOfSignature = verify_sign(publicKeyFileName, signature, message)
    print('\nverificationOfSignature: ', verificationOfSignature)