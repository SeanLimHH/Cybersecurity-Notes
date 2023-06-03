import random
import hashlib
lowercaseCharacterToAppend = 'abcdefghijklmnopqrstuvwxyz'
    
newValuesToStore = set()

with open('ex2_hash.txt','r') as reloadHashes:
    for line in reloadHashes:
        plaintext, hashedString = line.strip().split('|')
        characterToAppend = random.choice(lowercaseCharacterToAppend)
        saltedPlaintext = plaintext + characterToAppend
        saltedHash = hashlib.md5(saltedPlaintext.encode()).hexdigest()
        print(f'Random character to append: {characterToAppend}')
        print(f'Salted plain text: {saltedPlaintext}')
        print(f'Salted hash: {saltedHash}')
        newValuesToStore.add((saltedHash, characterToAppend, saltedPlaintext))

with open('salted6.txt','w') as saltedFileOut:
    with open('plain6.txt', 'w') as plainFileOut:
        for values in newValuesToStore:
            saltedHash, characterToAppend, saltedPlaintext = values
            saltedFileOut.write(saltedHash + '\n')
            plainFileOut.write(saltedPlaintext + '\n')