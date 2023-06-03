'''
Task context: Using brute force and given that we know a string is of 5 characters and is alphanumeric only, and
that alphabets are lowercase. The characters can repeat. The task is then to figure out the plaintext via brute-force.

Initially, i used import itertools.permutations. Which is not accurate for this task since we need replacement. But
permutations function assumes no replacement. I have to use itertools.product instead.
'''
from itertools import product #* Cannot use permutations; since permutations assumes no replacement.
from time import time
import hashlib
allPossibleCharacters = list("abcdefghijklmnopqrstuvwxyz0123456789")

hashesToCheck = set()
with open('hash5.txt','r') as hashes:
    for line in hashes:
        hashesToCheck.add(line.strip())

hashesFound = set()

start = time()

for plaintextTuple in product(allPossibleCharacters, repeat = 5):
    plaintextString = ''.join(plaintextTuple).strip()
    hashedValue = hashlib.md5(plaintextString.encode()).hexdigest()

    if len(hashesToCheck) == 0:
        print(f'Hashes to check {hashesToCheck}')
        print(f'Cumulative total time taken: {time()-start} seconds')
        break

    if hashedValue in hashesToCheck:
        timeElapsed = time() - start
        start = time()
        print(f'')
        print(f'Found plaintext for {hashedValue}: {plaintextString}')
        print(f'Time taken: {round(timeElapsed,2)} seconds')
        hashesFound.add((plaintextString, hashedValue, round(timeElapsed,2)))
        print(f'There are {len(hashesToCheck)} hashes left to brute-force!')
        hashesToCheck.discard(hashedValue)

print(f'\nBrute force completed. {len(hashesFound)} hashes were found. {len(hashesToCheck)} hashes were not found.')
print(f'Hashes found: {hashesFound}')
print(f'Hashes not found: {hashesToCheck}')

totalTimeTaken = 0
for hashedString in hashesFound:
    totalTimeTaken += hashedString[2]

totalTimeTaken = round(totalTimeTaken, 2)
averageTimeTaken = round(totalTimeTaken/len(hashesFound), 2)

print(f'\nTotal time taken: {totalTimeTaken} seconds')
print(f'\nAverage time taken: {averageTimeTaken} seconds')

with open('ex2_hash.txt', 'w') as fileOut:
    for hashedString in hashesFound:
        plaintext, plaintextHash, time = hashedString
        fileOut.write(plaintext + '|')
        fileOut.write(plaintextHash + '\n')
    
    print(f'\nDetails of all the breaked hashes has been written into file ex2_hash.txt successfully.')

counter = 1
with open('ex2_hash_more_info.txt', 'w') as fileOut:
    for hashedString in hashesFound:
        plaintext, plaintextHash, time = hashedString
        fileOut.write(str(counter)+'. Plaintext: '+ plaintext + '\n')
        fileOut.write('MD5 hashed value of plaintext: ' + plaintextHash + '\n')
        fileOut.write('Average time taken to brute-force this plaintext: ' + str(round(time,2)) + ' seconds.\n\n\n\n')
        counter += 1
    
    print(f'\nDetails of all the breaked hashes has been written into file ex2_hash_more_info.txt successfully.')