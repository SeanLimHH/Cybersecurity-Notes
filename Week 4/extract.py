'''
Background: The task was to "decrypt" an encrypted PBM file.

Some header information was given:
PBM file: 640 480, plaintext is either 0 or 1, no spaces.

The solution is to not solve it literally using code, but using visual inspection.
So a lot of the code below is to clean the cipher text to roughly see the image.

This is also the weakness of using Electronic Codebook Mode (ECB) for encrypting
plaintext (same key used => plaintext will have side-channel information).

As a result, the cipher text (image in this case) has patterns that can be seen.

64 bits => 8 bytes (8 bits per byte) due to ECB. So 8 bytes of plaintext are encrypted to 8 bytes.
With this in mind, i will begin a guess with 8 bytes per line.

PBM format => based on research it is found that for B/W 1 or 0 bits, we can assume that this output
image should have 480 bits => 480 columns and 640 bits => 640 row

Thus, based on header, it has 480 rows and 640 columns => 480 bits for each column and 640 bits for each row.

This means the binary decipher should be (640/8) bytes = 80 bytes

So when forming the image, one should use 80 bytes => 640 bits.

Since we replace in chunks of 8 bits, we do one byte.

With the hex dump, i am trying to form a pattern.
'''
import argparse


def getInfo(headerfile):
    with open(headerfile, 'r') as headerFile:
        lines = headerFile.readlines()
        return [lines[0], lines[2], '\n']

def extract(infile, outfile, headerfile, bytesPerLine = 8): #* Default to 8 bytes per line.
    frequency = {}
    with open(outfile, 'w') as outputFile:
        lines = getInfo(headerfile)
        for line in lines:
            outputFile.write(line)

    with open(outfile, 'ab') as outputFile:
        with open(infile, 'rb') as inputFile:
            while True:
                line = inputFile.read(bytesPerLine)
                if not line:
                    break
                if line not in frequency:
                    frequency[line] = 1
                else:
                    frequency[line] += 1
        
        '''
        #Usage of sorted:
        c = {'a':1,'b':4, 'd':3}
        c = sorted(c, key = lambda x: c[x], reverse = True) #* 'b', 'd', 'a'
        print(c)
        '''
        #* We want to replace common values to zero
        frequency = sorted(frequency, key = lambda x: frequency[x], reverse = True)
        with open(infile, 'rb') as inputFile:
            counter = 0
            while True:
                line = inputFile.read(bytesPerLine)
                if not line:
                    break
                if line in frequency[0]:
                    '''
                    We are doing an approximate replacement.

                    The idea is that based on the frequency of text, we replace a percentage
                    of the most repeated ones with '0'. 

                    This line: if line in frequency[:len(frequency)%x]:
                    The x => If it is a higher value, it is more lenient; else more strict
                    If more lenient, the image may not form (not enough replacement)
                    If more strict, the image will be more visible.
                    At maximum, it is simply 0. 

                    So, for the form frequency[:len(frequency)%x],
                    as x approaches 0, the image becomes more visible

                    This results in all repeated patterns to be
                    replaced and only extract out unique letters.
                    '''
                    outputFile.write(b'00000000')
                else:
                    outputFile.write(b'11111111')
                counter += 1
                if counter == 80: #* 80 bytes = 80 8-bit strings
                    outputFile.write(b'\n') #* We will need newlines. Because image has 640 rows
                    counter = 0
    

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    fileIn=args.infile
    fileOut=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%fileIn)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%fileOut)

    success=extract(fileIn,fileOut,headerfile)

            
