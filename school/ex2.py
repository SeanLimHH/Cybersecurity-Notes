#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out
'''
Context of exercise: Continuation of exercise 1. This part requires byte-wise now
instead of bit-wise. Idea remains. Difference now is that also, we can assume that
the whole encryption and decryption plays with the complete and full range of ASCII
values 0-255.
'''
import argparse

def encryptPrintable(fileIn, fileOut, key, info = 0):
    #* This was completed in part 1. Can ignore this for this exercise
    pass
    
def decryptPrintable(fileIn, fileOut, key, info = 0):
    #* This was completed in part 1. Can ignore this for this exercise
    pass
    
def encryptBinary(fileIn, fileOut, key, info = 0):
    if info:
        print("\nencryptBinary()")
        print(f"Input file: {fileIn}")
        print(f"Output file: {fileOut}")
        print(f"Key: {key}")

    with open(fileIn, mode = 'rb') as file:
        rawData = file.read()
    
    encryptedData = bytearray()
    if info:
        print(f"The whole raw data is {rawData}")

    for byte in rawData:
        if info:
            print(f"The byte in the data is {byte}.")
        encryptedByte = (byte + key) % 256 #* Handles overflow. Though the sherlock file should not have this case.
        encryptedData.append(encryptedByte)
    
    with open(fileOut, 'wb') as file: #* Writes one-shot the whole data
        file.write(encryptedData)

    if info:
        print("encryptBinary() completed successfully.")
   
def decryptBinary(fileIn, fileOut, key, info = 0):
    if info:
        print("\ndecryptBinary()")
        print(f"Input file: {fileIn}")
        print(f"Output file: {fileOut}")
        print(f"Key: {key}")

    with open(fileIn, mode = 'rb') as file:
        rawData = file.read()
    
    decryptedData = bytearray()
    if info:
        print(f"The whole raw data is {rawData}")

    for byte in rawData:
        if info:
            print(f"The byte in the data is {byte}.")
        decryptedByte = (byte - key) % 256 #* Handles overflow. Though the sherlock file should not have this case.
        #* negative % 256 will produce desired values.
        decryptedData.append(decryptedByte)
    
    with open(fileOut, 'wb') as file: #* Writes one-shot the whole data
        file.write(decryptedData)

    if info:
        print("decryptBinary() completed successfully.")

def validateKey(key):
    if key < 0 or key > 255:
        print("Please enter a valid key! It should be between 0 (inclusive) and 255 (inclusive)!")
        print('Exiting...')
        return False
    return True

def validateMode(mode):
    if mode != "e" and mode != "d" and mode != "f":
        print("Please enter a valid mode! It should either be 'e', 'd' or 'f'!")
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
    parser.add_argument("-m", "--mode", dest= "mode", help = "mode, either d, e or f")

    # parse our arguments
    args = parser.parse_args()
    fileIn = args.fileIn
    fileOut = args.fileOut
    key = args.key
    mode = args.mode.lower()
    if not validateKey(key) or not validateMode(mode):
        exit()

    if mode == "e":
        encryptBinary(fileIn, fileOut, key)
        #encryptBinary(fileIn, fileOut, key, info = 1)
        exit()
    if mode == "d":
        decryptBinary(fileIn, fileOut, key)
        #decryptBinary(fileIn, fileOut, key, info = 1)
        exit()
    if mode == "f": #* For solving the flag only. Key argument is irrelevant here.
        for key in range(256):
            newFileOutputName = "key" + str(key) + fileOut
            decryptBinary(fileIn, newFileOutputName, key)
        #* Afterwards, call 'file *' to quickly view the data types of all files in current folder
        #* Answer should be key 246 which shows a PNG image 1200 x 1200 of Switzerland flag
        exit()
