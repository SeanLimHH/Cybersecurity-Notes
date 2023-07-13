#---------------------------
# The context of this week's lab is to learn how the cryptographic hash
# algorithm works and its protocol.
#   
# The emphasis is on RSA as well.
# This exercise is to simulate an exchange using RSA encryption.
#---------------------------
from ex2 import *
if __name__ == '__main__':
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA256
    
    publicKey = open('mykey.pem.pub','r').read()
    alicePublicKey = RSA.importKey(publicKey)
    # public key
    #print(alicePublicKey.n)
    #print(alicePublicKey.e)
    
    # private key
    privateKey = open('mykey.pem.priv','r').read()
    alicePrivateKey = RSA.importKey(privateKey)
        
    #print(alicePrivateKey.n)
    #print(alicePrivateKey.d)
    s = random.getrandbits(1024) #* This is alice's message
    
    ciphertext = encryption(s, alicePublicKey.n, alicePublicKey.e)
    aliceSignature = square_multiply(ciphertext, alicePrivateKey.d, alicePrivateKey.n)
    print(f'\nAlice sends ciphertext:\n{ciphertext}')
    print(f'\nAlice sends her signature:\n{aliceSignature}')
    decryptedSignature = square_multiply(aliceSignature, alicePublicKey.e, alicePublicKey.n)
    print('\nBob uses the public key to verify alice\'s signature.')
    print(f'Bob obtains:\n\n{decryptedSignature}\n\nas the message.')
    print(f'\nIs this equal to the ciphertext?: {ciphertext == decryptedSignature}')
    if ciphertext == decryptedSignature:
        print(f'Since this it true, Bob accepts the pair (x,s):\n{ciphertext,aliceSignature}')
    else:
        print(f'Since this is false, Bob does not accept the pair (x,s):\n{ciphertext,aliceSignature}')