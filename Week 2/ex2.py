# Lab 2 Part II OTP

'''
Context of exercise:

Encrypt and decrypt using One-Time Pad (OTP)
Compromise the integrity of a OTP-encrypted message (if knowing the plain text)

'''
import os
import base64


def XOR(a, b): #* XOR loops through each character (of any encoding; converts into binary)
    #* Must take in bytes; example is a = b'hello', b = b'key'
    """Encryption using XOR, do not modify"""
    r = b""
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, "big")
    return r


def gen_OTP(length):
    """Generate a random OTP - you are not supposed to know the key - do not modify"""
    return bytearray(os.urandom(length))


def decrypt(cipher, OTP):
    """Decryption also using XOR, do not modify"""
    return XOR(cipher, OTP)


# Original message
original_plaintext = b"Student ID 1000000 gets 0 points\n"

# Randomly generated OTP
OTP = gen_OTP(length=len(original_plaintext))

# Encrypt
original_cipher = XOR(original_plaintext, OTP)

# Decrypt
# This will print the original message
print(decrypt(original_cipher, OTP))

def modifyByteOfCipher(original_cipher, index, newValue, info = 0):
    encodedValue = newValue.encode('utf-8')
    modifiedCipher = bytearray(original_cipher)
    if info:
        print(f'Value at index {index}: {modifiedCipher[index]}')

    for value in range(256): #* We need this because OTP is always changing => We need to figure what gives 4
        if (OTP[index]^value).to_bytes() == encodedValue: #* Ensure that when we XOR again we will get the string 4.
            if info:
                print(f'Value that yields {newValue}: {value}')
                print(f'Before change: {modifiedCipher}')
                print(f'Changing this value: {modifiedCipher[index].to_bytes()} to {value}')
            modifiedCipher[index] = value
            if info:
                print(f'After change: {modifiedCipher}')
            break
    return modifiedCipher

def main(info = 0):
    # TODO: manipulate ciphertext to decrypt to:
    # "Student ID 100XXXX gets 4 points"
    # Remember your goal is to modify the encrypted message
    # therefore, you do NOT decrypt the message here

    #* We have to manipulate the original cipher; the decryption will be done later.
    #* We just want to change the original cipher to a cipher with intending decrypted plaintext.

    #* We want to modify such that XOR(modified_cipher, OTP) yields 4
    #* Reverse of XOR is XOR itself.
    #* of the OTP with the modified cipher

    #* We can figure that the 24th position holds the value 0. We just literally change that to fit XOR
    #* Positions 14 - 17 contains student ID, position 24 is the 4 in '4 points'


    #* Since we need to do for student ID, i created a helper function to modify the cipher's byte

    #* Break down of each character in binary value: 
    modifiedCipher = bytearray(original_cipher)
    if info == 1:
        print(f'Original cipher: {original_cipher}')
        print(f'There are {len(original_cipher)} characters in the original plaintext')
        position = 0
        for c in modifiedCipher:
            print(f'Position {position}: {(c).to_bytes()}')
            position += 1

    studentID = '5954'

    currentByteIndex = 14
    for n in studentID:
        modifiedCipher = modifyByteOfCipher(modifiedCipher, currentByteIndex, n, info = 0)
        currentByteIndex += 1

    modifiedCipher = modifyByteOfCipher(modifiedCipher, 24, '4', info = 0)

    return modifiedCipher

new_cipher = main()

# When we finally decrypt the message, it should show the manipulated message
print(decrypt(new_cipher, OTP))
