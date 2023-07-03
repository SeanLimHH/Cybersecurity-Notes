'''
Context of this task: Efficiently computing (a^x) % n using the square and multiply algorithm.
Also compute whether a value is probably prime or not (Miller-Rabin algorithm).

The challenge here is slightly logical, slightly syntactical. There were difficulties reading
the wikipedia code and then implementing it as well (Miller-Rabin).
'''

import random


def getDecimal(binaryString):
    return int(binaryString,2)


def getBinary(decimalValue):
    return bin(decimalValue)[2:]

def convertBinaryStringToList(binaryString):
    if isinstance(binaryString, str):
        print('str')
        return list(binaryString)

    elif isinstance(binaryString, bytes):
        print('bytes')
        print(binaryString.decode())
        decodedBinaryInString = binaryString.decode()
        return list(decodedBinaryInString)
    
def convertListToString(binaryStringInList):
    return ''.join(c for c in binaryStringInList)
    
def convertListToDecimal(binaryStringInList):
    return int(''.join(str(c) for c in binaryStringInList),2)

def convertDecimalToList(decimalValue):
    return [int(v) for v in list(getBinary(decimalValue))]
        

def square_multiply(a,x,n): #* Is a tool to efficiently perform exponentiation operation.
    y = 1
    xBits = convertDecimalToList(x)
    for character in xBits:
        
        y = pow(y,2,n)
        if character == 1:
            y = a* y % n
    return y #* Result of the exponentiation


def miller_rabin(n, a): #* a is the number of rounds
    #* Algorithm following wikipedia: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # We want to factor out the 2s like this: n - 1 = 2^s * d
    s = 0 #* Power of 2 that is factored out
    d = n - 1 #* Leftover; original is the number n-1 itself.
    while d % 2 == 0: #* Factoring out powers of 2
        s += 1 #* Increase power of 2 that is factored out
        d //= 2 #* As we factor out the two, we need to reduce this by a power of 2 each time.

    # a = base rounds
    for round in range(a):
        a = random.randint(2, n - 2)
        x = pow(a, d, n) #* (a^d) % n

        for _ in range(s):
            y = pow(x, 2, n) #* x^2 % n
            if y == 1 and x != 1 and x != n-1:
                return False
            x = y

        if y != 1:
            return False

    return True


def gen_prime_nbits(n):
    #* This should generate up a prime number that consists of n bits
    number = random.getrandbits(n)
    while not miller_rabin(number, 2): #* checks if number is prime
        number = random.getrandbits(n)
    return number

if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
