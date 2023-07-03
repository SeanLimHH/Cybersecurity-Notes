'''
Context: The task(s) requires us to implement the Galois Field (GF) of two elements (GF2).
The challenge from this week's task(s) is syntax-related rather than logic.
'''

import copy


class Polynomial2:
    def __init__(self,coefficients):
        self.coefficients = coefficients 
    
    def longerLength(self, p2):
        if len(p2.coefficients) == len(self.coefficients):
            return 0
        
        if len(p2.coefficients) > len(self.coefficients):
            return p2

        if len(p2.coefficients) < len(self.coefficients):
            return self
    def getInt(self):
        total = 0
        index = 0
        while index != len(self.coefficients):
            total += self.coefficients[index] * (2**index)
            index += 1
        return total
    def resizeBitString(self, bitList, newSize):
        returnList = bitList.copy()
        toAdd = newSize - len(bitList)
        for zero in range(toAdd):
            returnList.append(0)
        return returnList
    
    def XOR(self,coefficient1, coefficient2):
        newCoefficientList = []
        
        if len(coefficient1) < len(coefficient2): #* This is smaller
            thisCoefficientsResized = self.resizeBitString(coefficient1,len(coefficient2))
            for index in range(len(thisCoefficientsResized)):
                newCoefficientList.append(thisCoefficientsResized[index]^coefficient2[index])
        elif len(coefficient1) > len(coefficient2): #* p2 is smaller
            p2CoefficientsResized = self.resizeBitString(coefficient2,len(coefficient1))
            for index in range(len(p2CoefficientsResized)):
                newCoefficientList.append(coefficient1[index]^p2CoefficientsResized[index])
        else:
            for index in range(len(coefficient1)):
                newCoefficientList.append(coefficient1[index]^coefficient2[index])
        
        return newCoefficientList    
    
    def AND(self,coefficient1, coefficient2):
        newCoefficientList = []
        
        if len(coefficient1) < len(coefficient2): #* This is smaller
            thisCoefficientsResized = self.resizeBitString(coefficient1,len(coefficient2))
            for index in range(len(thisCoefficientsResized)):
                newCoefficientList.append(thisCoefficientsResized[index]&coefficient2[index])
        elif len(coefficient1) > len(coefficient2): #* p2 is smaller
            p2CoefficientsResized = self.resizeBitString(coefficient2,len(coefficient1))
            for index in range(len(p2CoefficientsResized)):
                newCoefficientList.append(coefficient1[index]&p2CoefficientsResized[index])
        else:
            for index in range(len(coefficient1)):
                newCoefficientList.append(coefficient1[index]&coefficient2[index])
        
        return newCoefficientList
    
    def add(self,p2):
        newCoefficientList = []
        if len(self.coefficients) < len(p2.coefficients): #* This is smaller
            thisCoefficientsResized = self.resizeBitString(self.coefficients,len(p2.coefficients))
            for index in range(len(thisCoefficientsResized)):
                newCoefficientList.append(thisCoefficientsResized[index]^p2.coefficients[index])
        elif len(self.coefficients) > len(p2.coefficients): #* p2 is smaller
            p2CoefficientsResized = self.resizeBitString(p2.coefficients,len(self.coefficients))
            for index in range(len(p2CoefficientsResized)):
                newCoefficientList.append(self.coefficients[index]^p2CoefficientsResized[index])
        else:
            for index in range(len(self.coefficients)):
                newCoefficientList.append(self.coefficients[index]^p2.coefficients[index])
        
        return Polynomial2(newCoefficientList)
        
    def sub(self,p2):
        return self.add(p2)
        
    def mul(self,p2,modp=None):
        
        partialResults = [p2]
        for i in range(1,len(self.coefficients)):
            previousPartialResult = partialResults[-1] #* We get latest partial result

            previousPartialResult = Polynomial2([0] + previousPartialResult.coefficients) #* This is shift to the right.
            #* Increases power
            
            if modp is not None:
                if len(self.coefficients) == len(modp.coefficients): #* If same power then add
                    
                    partialResults.append(previousPartialResult)
                else:
                    #* First drop MSB then XOR
                    result = Polynomial2(previousPartialResult.coefficients[:-1])
                    result.add(Polynomial2(modp.coefficients[:-1]))
                    partialResults.append(result)
            else:
                partialResults.append(previousPartialResult)

        completeResult  = Polynomial2([0])
        index = 0
        for coefficient in self.coefficients:
            if coefficient == 1:
                completeResult = completeResult.add(partialResults[index])
            index += 1
        return completeResult  
    

    def leadingCoefficient(self):
        for c in range(len(self.coefficients)-1,-1,-1):
            if self.coefficients[c] == 1:
                return c

    def getDegree(self):
        for reverseIndex in range(len(self.coefficients)-1,-1,-1):
            if self.coefficients[reverseIndex] == 1:
                return reverseIndex


    def div(self, p2): #* self divide by p2
        quotient = Polynomial2([0])
        degree = p2.getDegree()
        remainder = copy.deepcopy(self)
        
        while remainder.getDegree() >= degree:
            newCoefficients = [0 for i in range(remainder.getDegree()-degree)] + [1]
            temp = Polynomial2(newCoefficients)
            remainder = remainder.sub(temp.mul(p2))
            quotient = temp.add(quotient)

        return quotient, remainder

    def toString(self):
        returnString = ''
        for backwardsIndex in range(len(self.coefficients),2,-1):
            print(f'backwardsIndex: {backwardsIndex}')
            if self.coefficients[backwardsIndex-1] == 1:
                returnString += f'+x^{backwardsIndex-1}'
        
        if self.coefficients[1] == 1:
            if len(returnString) >= 1:
                returnString += '+x'
            else:
                returnString += 'x'
            

        if self.coefficients[0] == 1:
            if len(returnString) >= 1:
                returnString += '+1'
            else:
                returnString += '1'
        else:
            if len(returnString) == 0:
                returnString += '0'
        print(returnString[1:])
        return returnString[1:]
    
    def __str__(self):
        returnString = ''
        for backwardsIndex in range(len(self.coefficients),2,-1):
            if self.coefficients[backwardsIndex-1] == 1:
                returnString += f'+x^{backwardsIndex-1}'
        if len(self.coefficients) >= 2:
            if self.coefficients[1] == 1:
                if len(returnString) >= 1:
                    returnString += '+x'
                else:
                    returnString += 'x'
            
        returnString = returnString[1:]
        if self.coefficients[0] == 1:
            if len(returnString) >= 1:
                returnString += '+1'
            else:
                returnString += '1'
        else:
            if len(returnString) == 0:
                returnString += '0'
        return returnString

    def getDec(self, binaryString):
        return int(binaryString,2)


    def getBin(self, decimalValue):
        return bin(decimalValue)[2:]

    def convertBinaryStringToList(self, binaryString):
        if isinstance(binaryString, str):
            print('str')
            return list(binaryString)

        elif isinstance(binaryString, bytes):
            print('bytes')
            print(binaryString.decode())
            decodedBinaryInString = binaryString.decode()
            return list(decodedBinaryInString)

    def convertListToString(self, binaryStringInList):
        return ''.join(c for c in binaryStringInList)
        
    def convertListToDecimal(self, binaryStringInList):
        return int(''.join([str(c) for c in binaryStringInList]),2)
    
    def convertDecimalToList(self, decimalValue):
        return [int(v) for v in list(self.getBin(decimalValue))]
        
class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.x = x #* Decimal value to be represented in GF(2)
        self.n = n
        self.ip = ip


    def add(self, g2):
        # XOR self using the add method and g2 without the msb
        
        XORResult = self.getPolynomial2().add(g2.getPolynomial2()) #* Add in polynomial2
        
        
        if len(XORResult.coefficients) == len(self.ip.coefficients):
            XORResult = Polynomial2(XORResult.coefficients[:-1]).add(Polynomial2(self.ip.coefficients[:-1]))
            #* Still must drop largest

        return GF2N(XORResult.getInt(), self.n, self.ip)
    
    
    def sub(self,g2):
        return self.add(g2)
    
    def mul(self,g2):
        result = self.getPolynomial2().mul(g2.getPolynomial2(), self.ip)
        return GF2N(result.getInt(),self.n,self.ip)

    def div(self,g2):
        quotientResult = self.getPolynomial2().div(g2.getPolynomial2())
        return GF2N(quotientResult[0].getInt(),self.n,self.ip), GF2N(quotientResult[1].getInt(),self.n,self.ip)

    def getPolynomial2(self):
        liste = list(bin(self.x)[2:])
        liste = liste[::-1]
        liste = [int(c) for c in liste]
        return Polynomial2(liste)

    def __str__(self):
        return str(self.getPolynomial2().getInt())

    def getInt(self):
        return self.getPolynomial2().getInt()


    def mulInv(self):
        
        
        return GF2N(self.getInt(), self.n, self.ip)

    def affineMap(self):
        thisPolynomial = self.getPolynomial2()
        currentCoefficients = []

        for i in range(len(thisPolynomial.coefficients)):
            temp = thisPolynomial.coefficients[i] ^ GF2N.affinemat[i][0]
            currentCoefficients.append(temp)
            for j in range(1, len(thisPolynomial.coefficients)):
                temp = thisPolynomial.coefficients[j] & GF2N.affinemat[i][j]
                currentCoefficients[-1] = currentCoefficients[-1] ^ temp
            
        return GF2N(Polynomial2(currentCoefficients).getInt(), self.n, self.ip)

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3=p1+p2 =',p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=',p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=',p8q)
print('r for p6/p7=',p8r)

####
print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ',g1.getPolynomial2())
print('g2 = ',g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ',g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 = ',g4.getPolynomial2())
print('g5 = ',g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 = ',g6.getPolynomial2())

print('\nTest 6')
print('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print('g7 = ',g7.getPolynomial2())
print('g8 = ',g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q = ',q.getPolynomial2())
print('r = ',r.getPolynomial2())

print('\nTest 7')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g9=GF2N(0b101,4,ip)
print('g9 = ',g9.getPolynomial2())
print('inverse of g9 =',g9.mulInv().getPolynomial2())

print('\nTest 8')
print('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print('irreducible polynomial',ip)
g10=GF2N(0xc2,8,ip)
print('g10 = 0xc2')
g11=g10.mulInv()
print('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print('affine map of g11 =',hex(g12.getInt()))
