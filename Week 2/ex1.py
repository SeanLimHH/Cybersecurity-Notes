#* Frequency of letters: https://blogs.sas.com/content/iml/2014/09/19/frequency-of-letters.html\
#* One can actually just do an ordering and do without the percentage values for the frequency.

'''
Context of exercise: Use frequency analysis + manual inspection to decrypt basic-encrypted text:
story_cipher.txt
'''
import argparse
import string
def frequencyMapping(fileIn, fileOut, info = 0):
    frequencyOfCharacters = {
    'E':12.49,'T':9.28,'A':8.04,'O':7.64,'I':7.57,'N':7.23, 'S':6.51,'R':6.28,'H':5.05,
    'L':4.07,'D':3.82,'C':3.34, 'U':2.73,'M':2.51,'F':2.40,'P':2.14,'G':1.87,'W':1.68,
    'Y':1.66,'B':1.48,'V':1.05,'K':0.54,'X':0.23,'J':0.16, 'Q':0.12, 'Z':0.09
    }
    if info == 1:
        print(f'Sorted frequency of characters {sorted(frequencyOfCharacters, key = lambda x: frequencyOfCharacters[x], reverse=True)}')
    standardFreqency = sorted(frequencyOfCharacters, key = lambda x: frequencyOfCharacters[x], reverse=True)
    computedFrequencyOfCharacters = {}
    with open(fileIn, mode='r') as inputFile:
            while True:
                character = inputFile.read(1)
                if not character:
                    break
                
                if character not in string.printable or (character not in frequencyOfCharacters.keys()):
                    continue

                if character not in computedFrequencyOfCharacters:
                    computedFrequencyOfCharacters[character] = 1
                else:
                    computedFrequencyOfCharacters[character] += 1
    if info == 1:
        print(f'Computed frequency: {computedFrequencyOfCharacters}')
        print(f'Sorted computed frequency of characters {sorted(computedFrequencyOfCharacters, key = lambda x: computedFrequencyOfCharacters[x], reverse=True)}')
    computedFrequency = sorted(computedFrequencyOfCharacters, key = lambda x: computedFrequencyOfCharacters[x], reverse=True)
    newMapping = {}
    
    for index in range(len(computedFrequency)):
        newMapping[computedFrequency[index]] = standardFreqency[index]

    with open(fileOut, mode = 'w') as outputFile:
        with open(fileIn, mode='r') as inputFile:
            while True:
                character = inputFile.read(1)
                
                if not character:
                    break
                
                if character in newMapping:
                    outputFile.write(newMapping[character])
                else:
                    outputFile.write(character)
    if info:
        print(f'File written to {fileOut}.')

def analysisHelper(fileIn,info = 0):
    if info == 1:
        print('Helper function for purely for manual and visual analysis.')
    
    wordFrequency = {}
    with open(fileIn, mode='r') as inputFile:
        data = inputFile.read()
        for word in data.split():
            if word not in wordFrequency:
                wordFrequency[word] = 1
            else:
                wordFrequency[word] += 1
    print('Words with one character:')
    for word in wordFrequency.keys():
        if len(word) == 1:
            print(word)
    
    print('Words with two characters:')
    for word in wordFrequency.keys():
        if len(word) == 2:
            print(word)

    print('Words with three characters:')
    for word in wordFrequency.keys():
        if len(word) == 3:
            print(word)

    print('Words that contain as many known characters, to be changed:')
    #* The following can be tweaked based on what you want to check.
    #* For example, if you know two letters, you can find a word with 3 or more characters that has the two letters.
    
    commonCharacters = {}
    for word in wordFrequency.keys():
        if 'A' in word and 'O' in word:
            if len(word) not in commonCharacters.keys():
                commonCharacters[len(word)] = [word]
            else:
                commonCharacters[len(word)].append(word)
     
    for numberOfCharacters, wordList in sorted(commonCharacters.items()):
        print(f'Number of characters: {numberOfCharacters}:',wordList)

    #* Additional criteria to analyse faster
    print('\n\n\nCriteria 2')
    commonCharacters = {}
    for word in wordFrequency.keys():
        if 'O' in word:
            if len(word) not in commonCharacters.keys():
                commonCharacters[len(word)] = [word]
            else:
                commonCharacters[len(word)].append(word)
     
    for numberOfCharacters, wordList in sorted(commonCharacters.items()):
        print(f'Number of characters: {numberOfCharacters}:',wordList)


    if info == 1:
        print('\n\n\n')

        print(f'Original: {wordFrequency}')
        print('\n\n\n')
        print(f'Sorted:', sorted(wordFrequency, key= lambda value: wordFrequency[value], reverse = True))
    

def manualMapping(fileIn, fileOut, info = 0):
    '''
    I ran this after reading the analysed text produced by the function above.
    Based on analysisHelper(); i figured that O and A is either A or I. If O is A, A is I. Similarly,
    If O is I, A is A
    

    The trick is to look for words that contain as many known characters, to make a more educated guess.
    
    Trying O as I, the text is not clear. So i will try O => A, A => I. This is clearer, so i will use this substitution.
    Reading the text: Guessing R == H
    Then H = R
    P = U
    At this stage, it is pretty easy to guess:
    I = O
    G is either T or W. Subbing T for now. Might change.
    C => G
    U => M
    W => F
    FRANMHISE => FRANCHISE? Then M => C
    IMYORTANTLF => IMPORTANTLY? Then Y => P, F = Y
    FOR BETTER FOR TORSE => T => W. This made the output worse so it is incorrect probably.

    At this stage, it is pretty readable. But there are some typos.
    Trying back the G => W, the text becomes more reasonable and readable.
    '''

    manualMap = {
        'O':'A',
        'A':'I',
        'R':'H',
        'H':'R',
        'P':'U',
        'I':'O',
        'G':'W',
        'C':'G',
        'U':'M',
        'W':'F',
        'M':'C',
        'Y':'P',
        'F':'Y',
    }
    if info == 1:
        print(f'Manual mapping: {manualMap}')
        print(f'Will write to file: {fileOut}')
    with open(fileOut, mode = 'w') as outputFile:
        with open(fileIn, mode='r') as inputFile:
            while True:
                character = inputFile.read(1)
                
                if not character:
                    break

                if character in manualMap:
                    outputFile.write(manualMap[character])
                else:
                    outputFile.write(character)
       

if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputFile",dest="fileIn", help="input file")
    parser.add_argument("-o", "--outputFile",dest="fileOut", help="output file")
    # parse our arguments
    args = parser.parse_args()
    fileIn = args.fileIn
    fileOut = args.fileOut

    #* The following maps basically to frequency
    frequencyMappedFileOut = 'frequency_' + fileOut
    frequencyMapping(fileIn, frequencyMappedFileOut)
    manualMapping(frequencyMappedFileOut, fileOut)

    #* The following line is just for visual manual analysis. You can ignore this.
    #analysisHelper(frequencyMappedFileOut)
