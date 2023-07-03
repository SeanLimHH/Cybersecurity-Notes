'''
Context: The task focuses here on implementing and encrypting a message via DHKE.
The main bulk and heavyweight rests and is implemented in primes.py. This task is
mainly using it.

The challenge i faced here was understanding what was needed to be done, the steps
and rough structure of how to implement the DHKE.
'''

import primes
import random
import babygiant
from cryptography.fernet import Fernet


def dhke_setup(nb):
    p = primes.gen_prime_nbits(nb)
    alpha = random.randint(2,p-2)
    return p, alpha 


def gen_priv_key(p):
    return random.randint(2, p-2)

def get_pub_key(alpha, a, p):
    return primes.square_multiply(alpha,a,p)


def get_shared_key(keypub, keypriv, p):
    return primes.square_multiply(keypub,keypriv,p)



if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())

    message ="Hello this is a message from A in plaintext."
    #message = "Hi"

    print("\nMessage that A is going to send to B:")
    print(message)

    print(f'\nShared key that is being used: {sharedKeyA}')
    key = Fernet.generate_key()
    f = Fernet(key)
    encryptedMessage = f.encrypt(message.encode())
    print(f"\nAfter encrypting using Fernet, the concatenated cipher text is: {encryptedMessage}")

    print(f'\nDecrypting using the same shared key:')
    
    decryptedMessage = f.decrypt(encryptedMessage, sharedKeyB)
    print(decryptedMessage.decode())
    
    
    print('\nSimulating an attack now...')
    import time
    for i in range(16,33):
        startTime = time.time()
        p, alpha = dhke_setup(i)
        privateKey = gen_priv_key(p)
        beta = get_pub_key(alpha,privateKey,p)
        realKey = get_shared_key(beta,privateKey,p)
        x = babygiant.baby_giant(alpha,beta,p)
        guessedKey = primes.square_multiply(beta,x,p)
        endTime = time.time()
        print(f"Key size: {i}")
        print(f"Guessed key: {guessedKey}")
        print(f"Real key: {realKey}")
        print(f"Time taken: {endTime-startTime} seconds.\n")
