'''
Context: The task here is to use the Shanks' Baby-step Giant-step method to solve the discrete
logarithm problem.
This discrete logarithm problem is formalised as finding x in alpha^x = beta, where 1 <= x <= p-1,
where p is a (very large) prime.
'''

import math
import primes

def sizeOfSquareRootOfG(p):
    return math.ceil(math.sqrt(p-1))

def baby_step(alpha, beta, p, fname):
    #* Alpha is generator g
    #* Beta is residue
    m = sizeOfSquareRootOfG(p)
    babySteps = {}

    for x in range(m):
        babySteps[x] = (beta * pow(alpha, x)) % p
    with open(fname, 'w') as outputFile:
        for index, step in babySteps.items():
            outputFile.write(f'{index},{step}\n')

def giant_step(alpha, p, fname):
    m = sizeOfSquareRootOfG(p)
    giantSteps = {}
    
    for x in range(m):
        giantSteps[x] = pow(alpha, (m*x), p)
    
    #* Checking
    babySteps = {}
    with open(fname, 'r') as babyStepFile:
        for line in babyStepFile:
            index, step = line.split(',')
            babySteps[int(index)] = int(step)
        
    for keyValuePairGiant in giantSteps.items():
        for keyValuePairBaby in babySteps.items():
            if keyValuePairGiant[1] == keyValuePairBaby[1]:
                return keyValuePairGiant[0]*m-keyValuePairBaby[0]
    return False #* Not found

def baby_giant(alpha, beta, p):
    fname = 'babySteps.txt'
    baby_step(alpha, beta, p, fname)
    x = giant_step(alpha,p, fname)
    return int(x)

if __name__ == "__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    """
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key :", sharedkey)
