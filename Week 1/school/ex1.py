#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


'''
Context of exercise: Practise shift ciphers and a bit of python.
Also basic encryption and decryption.
There is also focus on using argparse and command-prompt to run command-line code.

There is an input file. Calling
python ex1.py -i <input file> -o <output file> -k <key value> -m <mode> should, based
on mode (encryption or decryption), churn out the encrypted file or decrypt an
existing file. The encryption is based on Caesar cipher.

Some challenge includes that the keyset does not begin from 0, can be arbitrary. So
can its range.

'''

# Import libraries
import sys
import argparse
import string


def getKeySetInfo(keyset, info = 0):
    if info:
        print("\ngetKeySetInfo()")
        print(f"Returns ASCII numeric value in tuple: (max, min, max - min)")
    maximumASCIIValue = max([ord(c) for c in keyset])
    minimumASCIIValue = min([ord(c) for c in keyset])
    permissibleASCIIValues = maximumASCIIValue-minimumASCIIValue
    if info:
        print(f"Returning : {maximumASCIIValue, minimumASCIIValue, permissibleASCIIValues}")
    return (maximumASCIIValue, minimumASCIIValue, permissibleASCIIValues)

def encryptPrintable(fileIn, fileOut, key, info = 0):
    if info:
        print("\nencryptPrintable()")
        print(f"Input file: {fileIn}")
        print(f"Output file: {fileOut}")
        print(f"Key: {key}")
    outputFile = open(fileOut, mode = 'w', encoding='utf-8', newline="\n")
    with open(fileIn, mode = 'r', encoding='utf-8', newline="\n") as file:
        #* We must carefully handle the newlines as though they are a character itself.
        while True:
            #* Read 1 character at a time as-is. So spaces and newlines will be treated as normal character.
            c = file.read(1)
            if not c:
                if info:
                    print("\nReached end of file. Breaking out of while loop!")
                break
            
            if info:
                print(f"\nThis character is: {c}")
                print(f"The ASCII value for this character is {ord(c)}")

            if ord(c) >= minimumASCIIValue and ord(c) <= maximumASCIIValue:
                #* Ensure that we are only shifting values we SHOULD shift.
                if (ord(c) - minimumASCIIValue) + key > permissibleASCIIValues: #* Overflow case
                    newASCIIValue = (((ord(c) - minimumASCIIValue) + key) % permissibleASCIIValues) + minimumASCIIValue

                else: #* No overflow; normal case
                    newASCIIValue = ord(c) + key

                if info:
                    print(f"The key is {key}")
                    print(f"The ASCII value for this new encrypted character is {newASCIIValue}")
                    print(f"The new encrypted character is: {chr(newASCIIValue)}")

                outputFile.write(chr(newASCIIValue))
            else:
                if info:
                    print(f'Character outside character set detected: {c}')
        if info:
            print("encryptPrintable() completed successfully.")
    
def decryptPrintable(fileIn, fileOut, key, info = 0):
    if info:
        print("\ndecryptPrintable()")
        print(f"Input file: {fileIn}")
        print(f"Output file: {fileOut}")
        print(f"Key: {key}")
    outputFile = open(fileOut, mode = 'w', encoding='utf-8', newline="\n")
    with open(fileIn, mode = 'r', encoding='utf-8', newline="\n") as file:
        #* We must carefully handle the newlines as though they are a character itself.
        while True:
            #* Read 1 character at a time as-is. So spaces and newlines will be treated as normal character.
            c = file.read(1)
            if not c:
                if info:
                    print("\nReached end of file. Breaking out of while loop!")
                break
            
            if info:
                print(f"\nThis character is: {c}")
                print(f"The ASCII value for this character is {ord(c)}")

            if ord(c) >= minimumASCIIValue and ord(c) <= maximumASCIIValue:
                #* Ensure that we are only shifting values we SHOULD shift.
                if (ord(c) - minimumASCIIValue) < key: #* Implies overflowed
                    newASCIIValue = ((ord(c)-minimumASCIIValue) - key) % maximumASCIIValue
                
                else: #* No overflow; normal case
                    newASCIIValue = ord(c) - key

                if info:
                    print(f"The new decrypted character is: {chr(newASCIIValue)}")
                    print(f"The key is {key}")
                    print(f"The ASCII value for this decrypted character is {newASCIIValue}")

                outputFile.write(chr(newASCIIValue))
            else:
                if info:
                    print(f'Character outside character set detected: {c}')
    if info:
        print("decryptPrintable() completed successfully.")
    
def encryptBinary(fileIn, fileOut, key):
    #* To be done in ex2.py
    outputFile = open(fileOut, mode = 'wb')
    with open(fileIn, mode = 'rb') as file:
        pass
    
def decryptBinary(fileIn, fileOut, key):
    #* To be done in ex2.py
    outputFile = open(fileOut, mode = 'wb')
    with open(fileIn, mode = 'rb') as file:
        pass

def validateKey(key):
    if key < 1 or key > len(string.printable)-1:
        print(f"Please enter a valid key! It should be between 1(inclusive) and {len(string.printable)-1}(inclusive)!")
        print('Exiting...')
        return False
    return True

def validateMode(mode):
    if mode != "e" and mode != "d":
        print("Please enter a valid mode! It should either be 'e' or 'd'")
        print('Exiting...')
        return False
    return True

# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputFile",dest="fileIn", help="input file")
    parser.add_argument("-o", "--outputFile",dest="fileOut", help="output file")
    parser.add_argument("-k", "--key", default = 1, type = int, dest= "key", help = "key")
    parser.add_argument("-m", "--mode", dest= "mode", help = "mode, either d or e")

    # parse our arguments
    args = parser.parse_args()
    fileIn = args.fileIn
    fileOut = args.fileOut
    key = args.key
    mode = args.mode.lower()
    if not validateKey(key) or not validateMode(mode):
        exit()
    
    #* The following line will be used in the future lines.
    maximumASCIIValue, minimumASCIIValue, permissibleASCIIValues = getKeySetInfo(string.printable)
   
    if mode == "e":
        encryptPrintable(fileIn, fileOut, key)
        exit()
    if mode == "d":
        decryptPrintable(fileIn, fileOut, key)
        exit()

