'''
Background: Implementing the PRESENT cipher to familiarise with block ciphers.
https://www.iacr.org/archive/ches2007/47270450/47270450.pdf

Majority of the difficulty was syntax-related; how to manipulate the bytes, bits
and hexadecimals in Python.
'''
#* Helper functions
def convertBitStringToInteger(bitString, base):
    #* Converts both '0110' and b0110 variations to actual integer.
    if isinstance(bitString,int):
        return int(bitString)
    else:
        return int(bitString, base)
    
def convertIntegerToBitString(integer, hasPrefix = 0):
    if hasPrefix == 1:
        return bin(integer)
    return bin(integer)[2:]

def convertBitStringToHexadecimal(bitString, base):
    #* Bit string can be either in the form of '1101' or 0b1101
    if isinstance(bitString,int):
        return hex(bitString)
    else:
        return hex(int(bitString,base))

def convertHexadecimalToBinary(hexadecimal, hasPrefix = 0):
    #* Convert 0xd to 0b1101 or "1101"
    if hasPrefix == 1:
        if isinstance(hexadecimal, int):
            return bin(int(hexadecimal))
        elif isinstance(hexadecimal, str):
            return bin(int(hexadecimal,16))
    else:
        if isinstance(hexadecimal, int):
            return bin(int(hexadecimal))[2:]
        elif isinstance(hexadecimal, str):
            return bin(int(hexadecimal,16))[2:]

def resizeBitString(bitString, newSize):
    return f'{bitString:0{newSize}b}'

def concatenateBinaryStrings(leftString, rightString, info = 0):
    if (isinstance(leftString, int) and isinstance(rightString, int)) or \
    (isinstance(leftString, str) and isinstance(rightString, str)):
        if info:
            print(f'Left string input: {leftString}')
            print(f'Right string input: {rightString}')
            print(f'Both data type is: {type(leftString)}')
        if isinstance(leftString, int): #* Data type of both is of the form 0b1001
            print("Error. Data type should be of form '1001' but received 0b1001 instead.")
        elif isinstance(leftString, str): #* Data type of both is of the form '1001
            return leftString + rightString
    else:
        print('Inconsistent data type.')
        return False

#* End of helper functions


FULLROUND = 31

sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

pLayerSubstitution = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
       4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
       8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
       12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

# Rotate left: 0b1001 --> 0b0011
def rol(val, r_bits, max_bits): return \
    (val << r_bits % max_bits) & (2**max_bits - 1) | \
    ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

# Rotate right: 0b1001 --> 0b1100
def ror(val, r_bits, max_bits): return \
    ((val & (2**max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1))

def genRoundKeys(key, info = 0):
    K = {0:32}
    if info:
        print('genRoundKeys()')
    keyRegister = key
    for i in range(1, FULLROUND+2,1): #* We want i to be [1,32]
        if info:
            print(f'\nRound {i}')
            print(f"Start of round key register: {bin(keyRegister)}")
        K[i] = keyRegister >> 16 #* Removes right-most 16 bits. This will thus be the round's key.
        if info:
            print(f"Value of round key for this round: {bin(K[i])}")
        keyRegister = rol(keyRegister,61,80) #* Manipulation of keyRegister, rotate 61 bits anticlockwise.

        if info:
            print(f'Key register before sbox, rotated: {bin(keyRegister)}')
        
        leftMost4BitsInDecimal = keyRegister >> 76
        if info:
            print(f'leftMost4BitsInDecimal: {leftMost4BitsInDecimal}')
        fullOnes = "1"*76
        rightStringToConcatenate = keyRegister & int(fullOnes,2)
        if info:
            print(f'rightStringToConcatenate: {rightStringToConcatenate}')
        keyRegister = (sbox[leftMost4BitsInDecimal]<<76) | rightStringToConcatenate
        if info:
            print(f'Round counter, originally is: {bin(i)}')
            print(f'Round counter, shifted 15 to the left is: {bin(i<<15)}')
        keyRegister = keyRegister ^ (i << 15) #* Adds 15 trailing zeroes to i, then XORs it with keyRegister.
        if info:
            print(f'Final value of key register at end of this round: {bin(keyRegister)}')
    if info:
        print(f'Returning value {K}')
    return K

def addRoundKey(state, Ki):
    return state^Ki

def sBoxLayer(state, info = 0):
    if info:
        print('sBoxLayer()')
    updatedState = ""
    state = f'{state:064b}'
    for i in range(0, 64, 4):
        hexadecimal = state[i:i+4]
        hexadecimalValueInDecimal = int(hexadecimal, 2)
        updatedState += f'{sbox[hexadecimalValueInDecimal]:04b}'
        if info:
            print(f'Updated state: {updatedState}')
    if info:
        print(f'sBoxLayer returns: {updatedState}')
    return updatedState

sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
def sBoxLayerInverse(state, info = 0):
    if info:
        print('sBoxLayerInverse()')
    sBoxInverse = []
    sBoxInverseIndex = 0
    while sBoxInverseIndex != len(sbox):
        sboxIndex = 0
        for hexadecimal in sbox:
            if resizeBitString(hexadecimal,4) == resizeBitString(sBoxInverseIndex,4):
                sBoxInverse.append(sboxIndex)
            sboxIndex += 1
        sBoxInverseIndex += 1
        
    if info:
        print(f'sBoxInverse table built:\n{sBoxInverse}')
    substitution = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    for number in range(len(sBoxInverse)):
        if sBoxInverse[number] >= 10:
            sBoxInverse[number] = substitution[sBoxInverse[number]]
    
    if info:
        print(f'Updated sBoxLayerInverse table:\n{sBoxInverse}')
    updatedState = ''
    state = f'{state:064b}'
    for i in range(0, 64, 4):
        hexadecimal = state[i:i+4]
        hexadecimalValueInDecimal = int(hexadecimal, 2)
        updatedState += str(sBoxInverse[hexadecimalValueInDecimal])
        if info:
            print(f'Updated state: {updatedState}')
    if info:
        print(f'sBoxInverse returns: {int(updatedState,16)}')
    return int(updatedState,16)

def pLayer(state, info = 0):
    if info:
        print(f'pLayer()')
    newState = [-1 for x in range(64)] #* -1 is a dummy value
    counter = 0
    for character in state:
        newState[pLayerSubstitution[counter]] = character
        counter += 1
    counter = 0
    afterPLayerSubstitutionInBits = ''.join(newState)
    if info:
        print(f'After the pLayer is applied: {int(afterPLayerSubstitutionInBits,2)}')
    return int(afterPLayerSubstitutionInBits,2)

def pLayerInverse(state, info = 0):
    if info:
        print(f'pLayerInverse()')
    pLayerSubstitutionInverse = []
    
    if (64-len(state)) > 0:
        paddingZeroes = "0"*(64-len(state))
        state = paddingZeroes + state
    remapIndex = 0
    while remapIndex != len(pLayerSubstitution):
        pLayerSubstitutionIndex = 0
        for index in pLayerSubstitution:
            if remapIndex == index:
                pLayerSubstitutionInverse.append(pLayerSubstitutionIndex)
            pLayerSubstitutionIndex += 1
        remapIndex += 1
    if info:
        print(f'pLayerSubstitutionInverseTable built:\n{pLayerSubstitutionInverse}')
    newState = [-1 for x in range(64)] #* -1 is a dummy value
    counter = 0
    for character in state:
        newState[pLayerSubstitutionInverse[counter]] = character
        counter += 1
    counter = 0
    for c in newState:
        if c == -1:
            print(counter)
        counter += 1
    for i in range(64):
        if i not in pLayerSubstitutionInverse:
            print(i)
    afterPLayerSubstitutionInBits = ''.join(newState)
    if info:
        print(f'pLayerInverse returns: {int(afterPLayerSubstitutionInBits,2)}')
    return int(afterPLayerSubstitutionInBits,2)

def present_round(state, roundKey):
    #* Round key is K_i (technically K[i]). It should thus contain 64 bits.
    state = addRoundKey(state, roundKey)
    state = sBoxLayer(state)
    state = pLayer(state)
    return state


def present_inv_round(state, roundKey):
    state = bin(state)[2:] #* We want the form "1001" instead of 0b1001
    state = pLayerInverse(state)
    state = sBoxLayerInverse(state)
    state = addRoundKey(state, roundKey)
    return state


def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    print(f'present returns {hex(state)}')
    print(f'present returns {state}')
    return state


def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    print(f'present_inv returns {hex(state)}')
    print(f'present_inv returns {state}')
    return state

if __name__ == "__main__":
    # Testvector for key schedule
    key1 = 0x00000000000000000000 #* 80 bits, 20 bytes
    keys = genRoundKeys(key1)
    keysTest = {0: 32, 1: 0, 2: 13835058055282163712, 3: 5764633911313301505, 4: 6917540022807691265, 5: 12682149744835821666, 6: 10376317730742599722, 7: 442003720503347, 8: 11529390968771969115, 9: 14988212656689645132, 10: 3459180129660437124, 11: 16147979721148203861, 12: 17296668118696855021, 13: 9227134571072480414, 14: 4618353464114686070, 15: 8183717834812044671, 16: 1198465691292819143, 17: 2366045755749583272, 18: 13941741584329639728, 19: 14494474964360714113, 20: 7646225019617799193, 21: 13645358504996018922, 22: 554074333738726254, 23: 4786096007684651070, 24: 4741631033305121237, 25: 17717416268623621775, 26: 3100551030501750445, 27: 9708113044954383277, 28: 10149619148849421687, 29: 2165863751534438555, 30: 15021127369453955789, 31: 10061738721142127305, 32: 7902464346767349504}
    for k in keysTest.keys():
        assert keysTest[k] == keys[k]
    
    # Testvectors for single rounds without keyscheduling
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    round1 = present_round(plain1, key1)
    round11 = 0xffffffff00000000
    assert round1 == round11
    round2 = present_round(round1, key1)
    round22 = 0xff00ffff000000
    assert round2 == round22

    round3 = present_round(round2, key1)
    round33 = 0xcc3fcc3f33c00000
    assert round3 == round33

    # invert single rounds
    plain11 = present_inv_round(round1, key1)
    print(f'plain1: {plain1}')
    print(f'plain1 in hex: {hex(plain1)}')
    print(f'plain11: {plain11}')
    print(f'plain11 in hex: {hex(plain11)}')
    assert plain1 == plain11
    plain22 = present_inv_round(round2, key1)
    print(f'round1: {round1}')
    print(f'round1 in hex: {hex(round1)}')
    print(f'plain22: {plain22}')
    print(f'plain22 in hex: {hex(plain22)}')
    assert round1 == plain22
    plain33 = present_inv_round(round3, key1)
    assert round2 == plain33
    print("\n\n\n\n\n")
    # Everything together
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    cipher1 = present(plain1, key1)
    plain11 = present_inv(cipher1, key1)
    print(f'plain1: {plain1}')
    print(f'plain1 in hex: {hex(plain1)}')
    print(f'plain11: {plain11}')
    print(f'plain11 in hex: {hex(plain11)}')
    assert plain1 == plain11

    plain2 = 0x0000000000000000
    key2 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher2 = present(plain2, key2)
    plain22 = present_inv(cipher2, key2)
    assert plain2 == plain22

    plain3 = 0xFFFFFFFFFFFFFFFF
    key3 = 0x00000000000000000000
    cipher3 = present(plain3, key3)
    plain33 = present_inv(cipher3, key3)
    assert plain3 == plain33

    plain4 = 0xFFFFFFFFFFFFFFFF
    key4 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher4 = present(plain4, key4)
    plain44 = present_inv(cipher4, key4)
    assert plain4 == plain44
    print('Test cases all passed.')