#---------------------------
# The context of this week's lab is to learn how the cryptographic hash
# algorithm works and its protocol.
#   
# The emphasis is on RSA as well.
# This exercise is to simulate an RSA encryption protocol attack on encryption
# implementation without padding.
#---------------------------
from ex2 import *

if __name__ == '__main__':
    from Crypto.PublicKey import RSA
    
    publicKey = open('mykey.pem.pub','r').read()
    publicKey = RSA.importKey(publicKey)
    # public key
    #print(publicKey.n)
    #print(publicKey.e)
    with open('message.txt', 'r') as file:
        message = file.read()
        
    # private key
    privateKey = open('mykey.pem.priv','r').read()
    privateKey = RSA.importKey(privateKey)
    
    chosenInteger = 18
    ciphertext = square_multiply(chosenInteger, publicKey.e, publicKey.n)
    chosenMultiplier = 2
    ciphertextMultiplied = square_multiply(chosenMultiplier, publicKey.e ,publicKey.n)
    multipliedResult = ciphertext * ciphertextMultiplied
    decryptedPlaintext = decryption(multipliedResult, privateKey.n, privateKey.d)
    
    print("Part II-------------")
    print(f"Encrypting: {chosenInteger}")
    print("Result")
    print(ciphertext)
    print(f"Decrypted: {decryptedPlaintext}")

