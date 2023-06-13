'''
Background: Use Electronic Codebook Mode (ECB) for encrypting plaintext (image in this case).
Also uses a bit of block cipher (implementation through PRESENT).

The idea for this is not too difficult; divide the whole file's bytestring into chunks
that the cryptographic block cipher can handle. Then, encrypt each block.

The limitation is that the same key is used to encrypt each block. This results in some
similarity and less randomness. 
'''


from present import *
import argparse

nokeybits=80
blocksize=64

def encryptOneBlock(block, key): #* Input in just a singular block with the corresponding key
    return present_round(block, key)

def decryptOneBlock(cipherBlock, key): #* Input in just a singular block with the corresponding key
    return present_inv_round(cipherBlock, key)

def ecb(infile, outfile, key, mode):
    if mode == 'e':
        with open(outfile, 'wb') as outputFile:
            with open(infile,'rb') as inputFile:
                while True:
                    block = int.from_bytes(inputFile.read(8))
                    if not block:
                        break
                    outputFile.write((encryptOneBlock(block, key)).to_bytes(8))
            
    if mode == 'd':
        with open(outfile, 'wb') as outputFile:
            with open(infile,'rb') as inputFile:
                while True:
                    block = int.from_bytes(inputFile.read(8))
                    if not block:
                        break
                    outputFile.write((decryptOneBlock(block, key)).to_bytes(8))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    fileIn=args.infile
    fileOut=args.outfile
    key=args.keyfile
    mode = args.mode.lower()
    ecb(fileIn, fileOut, int(key), mode = mode)
