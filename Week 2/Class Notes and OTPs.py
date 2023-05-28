'''Here i am just playing with the XOR in lecture slides'''

a = 0b11100101
print('a:', a) #* Returns decimal value
print('Binary of a:', bin(a)) #* Returns 0b11100101, the typical "desired" string

b = 0b10111011
print('b:', b) #* Returns decimal value
print('Binary of b:', bin(b)) #* Returns 0b11100101, the typical "desired" string

aXORb = a ^ b #* Bit algorithm idea: Same => '0'; Different => '1'
print("XOR output:", bin(aXORb))

#* Representing binary as ASCII
rawBinaryStringOfA = bin(a)[2:] #* Remove the '0b' prefix

#* With the bit algorithm above, to reverse an XOR operator:
#* Assume that initially there are two strings A and B which are XORed.
#* For the 1s: Either string A or string B has 1, the other has 0, vice-versa.
#* For the 0s: Either both strings A and B has 0, or both strings has 1.

#* Based on this analysis, for each position, if the XOR output is:
#* 0 => There are 2 possibilities, permutations. => 0 1 or 1 0
#* 1 => There are 2 possibilities, permutations. => 1 1 or 0 0
#* Therefore, for two binary strings of N-bits that are XORed, there are 2^N possibilities.
#* This assumes the XOR is bit-wise, and not in blocks

possibleABStrings = {}
position = 0
print('Binary output just bits:', rawBinaryStringOfA)

for outputBit in rawBinaryStringOfA:
    possibleABStrings[position] = []

    if outputBit == "0":
        #* (1, 0) corresponds to this index of string A to string B: (A, B) == (1, 0)
        possibleABStrings[position].append((1,0))
        possibleABStrings[position].append((0,1))
    
    elif outputBit == "1":
        possibleABStrings[position].append((0,0))
        possibleABStrings[position].append((1,1))

    position += 1

for position in possibleABStrings:
    print(f"Position {position}: {possibleABStrings[position]}")


#* From ChatGPT: Cyclic Redundancy Check (CRC) is a checksum algorithm.
#* The following implementation is not in syllabus; is just for my knowledge
#* Polynomial division approach

exampleData = '101101001'

#* The task will be to create a checksum for this exampleData, to ensure that it is
#* transmitted successfully.

#* The concept of CRC polynomial division approach is to create a remainder based on
#* the input data AND a chosen generator polynomial.

import random
import string

oneTimePadAlphaNumeric = ''
for c in range(len(exampleData)):
    oneTimePadAlphaNumeric += string.printable[random.randint(0,len(string.printable))]

oneTimePadNumeric = ''
for c in range(len(exampleData)):
    oneTimePadNumeric += str(random.randint(0,1))
print(f'Original string:{exampleData}')
print(f'One-time pad:{oneTimePadNumeric}')

result = ''
for c in range(len(exampleData)):
    result += str(int(exampleData[c]) ^ int(oneTimePadNumeric[c]))
print(f'Result:{result}')

#* An ideal cipher using one-time pad requires a 0.5 probability of each position being either a 0 or 1. Because of the nature of XOR, this is possible 



#*-------------------------------------------------------------------------------------------------------------------------------------------------------
#* Confidentiality does not imply integrity => we need a dedicated way to ensure that the message's integrity is enforced => Cryptographic hash functions