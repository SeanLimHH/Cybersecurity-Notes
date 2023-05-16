plainText = "secret test word that should not be revealed"
print('Plain text:',plainText)
def mapString(plainText, mapping):
    mappedList = [mapping.get(char, char) for char in plainText]
    cipherText = ''.join(mappedList)
    return cipherText

import matplotlib.pyplot as plt
def frequencyChart(string):
    frequency = {}
    for char in string:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # Extracting the character frequencies and labels
    characters = list(frequency.keys())
    frequencies = list(frequency.values())

    # Plotting the bar graph
    plt.bar(characters, frequencies)
    plt.xlabel("Characters")
    plt.ylabel("Frequency")
    plt.title("Character Frequency Chart")

    # Displaying the graph
    plt.show()
    return frequency

'''Simple substitution: Caesar Cipher
Example is like shifting 3 alphabets down the standard a->b->c->d...->x->y->z.
'''
simpleSubstitutionMapping = {
        'a': 'b',
        'b': 'd',
        'c': 'e',
        'd': 'c',
        'e': 'a',
        'f': 'g',
        'g': 'i',
        'h': 'j',
        'i': 'h',
        'j': 'f',
        'k': 'l',
        'l': 'n',
        'm': 'o',
        'n': 'm',
        'o': 'k',
        'p': 'q',
        'q': 's',
        'r': 't',
        's': 'r',
        't': 'p',
        'u': 'v',
        'v': 'x',
        'w': 'y',
        'x': 'w',
        'y': 'u',
        'z': 'a',
        ' ': ' '}

cipherText = mapString(plainText, simpleSubstitutionMapping)
print("\nBasic substitution cipher text:", cipherText)
frequencyChart(cipherText)

'''Vigenère cipher is best thought of:
The Vigenère cipher is akin to a password manager with multiple accounts. Each
account represents a letter in the message, and the passwords used for each account 
are derived from a keyword. By generating unique passwords based on the keyword, 
the password manager secures each account with different combinations. 

The total number of possible combinations, or the keyspace, grows exponentially with
the length of the keyword. Only those who possess the correct keyword can access the
password manager and unlock the original message hidden within the encrypted accounts
, utilizing the vast keyspace to ensure security.

The idea: It composes of the simple substitution method above, but having multiple 
variations. I understand that they use letters for the encryption, but here i am using
numbers
'''
vigenerePatterns = {
    '1': {
        'a': 'b',
        'b': 'd',
        'c': 'e',
        'd': 'c',
        'e': 'a',
        'f': 'g',
        'g': 'i',
        'h': 'j',
        'i': 'h',
        'j': 'f',
        'k': 'l',
        'l': 'n',
        'm': 'o',
        'n': 'm',
        'o': 'k',
        'p': 'q',
        'q': 's',
        'r': 't',
        's': 'r',
        't': 'p',
        'u': 'v',
        'v': 'x',
        'w': 'y',
        'x': 'w',
        'y': 'u',
        'z': 'a',
        ' ': ' '},


    '2': {
        'a': 'c',
        'b': 'e',
        'c': 'g',
        'd': 'i',
        'e': 'k',
        'f': 'm',
        'g': 'o',
        'h': 'q',
        'i': 's',
        'j': 'u',
        'k': 'w',
        'l': 'y',
        'm': 'a',
        'n': 'b',
        'o': 'd',
        'p': 'f',
        'q': 'h',
        'r': 'j',
        's': 'l',
        't': 'n',
        'u': 'p',
        'v': 'r',
        'w': 't',
        'x': 'v',
        'y': 'x',
        'z': 'z',
        ' ': ' '},

    '3': {
        'a': 'd',
        'b': 'g',
        'c': 'j',
        'd': 'm',
        'e': 'p',
        'f': 's',
        'g': 'v',
        'h': 'y',
        'i': 'b',
        'j': 'e',
        'k': 'h',
        'l': 'k',
        'm': 'n',
        'n': 'q',
        'o': 't',
        'p': 'w',
        'q': 'z',
        'r': 'c',
        's': 'f',
        't': 'i',
        'u': 'l',
        'v': 'o',
        'w': 'r',
        'x': 'u',
        'y': 'x',
        'z': 'a',
        ' ': ' '}

}

import random
random.seed(0)
cipherText = ''
for c in plainText:
    randomNumberKey = str(random.randint(1,3))
    cipherText += mapString(c, vigenerePatterns[randomNumberKey])
    
print("\nVigenere cipher text:", cipherText)
frequencyChart(cipherText)