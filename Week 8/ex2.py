#---------------------------
# The context of this week's lab is to learn how the cryptographic hash
# algorithm works and its protocol.
#   
# The emphasis is on RSA as well.
# This exercise is to simulate RSA without padding
#---------------------------
import random

def getBinary(decimalValue):
    return bin(decimalValue)[2:]

def convertDecimalToList(decimalValue):
    return [int(v) for v in list(getBinary(decimalValue))]

def square_multiply(a,x,n): #* Is a tool to efficiently perform exponentiation operation.
    y = 1
    xBits = convertDecimalToList(x)
    for character in xBits:
        
        y = pow(y,2,n)
        if character == 1:
            y = a* y % n
    return y #* Result of the exponentiation


def encryption(plaintext, modulus, encryptionExponent):
    if isinstance(plaintext, int):
        return square_multiply(plaintext, encryptionExponent, modulus)
    plaintextArray = [ord(char) for char in plaintext]
    ciphertextArray = [square_multiply(message, encryptionExponent, modulus) for message in plaintextArray]
    return ciphertextArray
    
def decryption(ciphertextArray, modulus, decryptionExponent):
    if isinstance(ciphertextArray, int):
        return square_multiply(ciphertextArray, decryptionExponent, modulus)
    plaintextArray = [square_multiply(ciphertext, decryptionExponent, modulus) for ciphertext in ciphertextArray] 
    plaintextArray = [chr(char) for char in plaintextArray]
    return (''.join(plaintextArray))
    
if __name__ == '__main__':
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA256
    
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
        
    #print(privateKey.n)
    #print(privateKey.d)

    hashObject = SHA256.new()
    hashObject.update(message.encode())
    print(f"\nHashed value of plaintext == ciphertext: {hashObject.hexdigest()}")
    signature = encryption(hashObject.hexdigest(), privateKey.n, privateKey.d)
    decryptedSignature = decryption(signature, publicKey.n, publicKey.e)
    print(f"Decrypted signature == ciphertext: {decryptedSignature}")
    print(f"Verification of signature returns: {hashObject.hexdigest() == decryptedSignature}")