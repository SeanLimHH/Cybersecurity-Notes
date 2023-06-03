'''
The goal of this week is to learn MD5 hashing and cracking using brute force and rainbow tables.
Also to learn how to salt and then attempting to crack it nonetheless.
The tool that will be used will be rainbow crack; but the focus is on using other rainbow tables, not just this one
'''

'''
Two ways to generate MD5 hashes
1. Shell: echo -n "plaintextToBeHashed" | md5sum
2. Python script (see below)
'''
import hashlib

plaintext = 'plaintextToBeHashed'.encode()
result = hashlib.md5(plaintext)
print(result.hexdigest())

for i in range(1,10):
    plaintext = i*'a'
    print(f'\nPlaintext: {plaintext}')
    hashedValue = hashlib.md5(plaintext.encode()).hexdigest()
    print(f'Hash value: {hashedValue}')
    print(f'Length of hash: {len(hashedValue)}')

'''
The first task is to figure whether the length of hash correspond to input string. Some general understanding about MD5 hashes.

The second task is to brute-force MD-5 of certain characteristics. See ex2.py.

The third task is to learn how to use rainbow tables to recover MD5-hashes' plaintexts. 
We also use to create rainbow tables of desired paramters.

The fourth task is to redo the third task, with now salting in mind. We will still use rainbow tables. See ex4.py.

We are using project rainbow crack as example (to simulate using a rainbow table attack). You have to first install it.

Here we begin by generating a rainbow table of required parameters (parameters detailed and explained in school homework): 
./rtgen md5 loweralpha-numeric 5 5 0 3800 600000 0
This churns a rainbow table with chain number of 600000 and chain length of 3800. Minimum and maximum character length of 5.

Details on above: https://security.stackexchange.com/questions/194614/to-build-a-rainbow-table-how-to-decide-size-of-chain-and-number-of-lines#:~:text=The%20chain%20length%20is%20basically,chain%20count%20is%20basically%20coverage

The chain length is basically time. A longer chain takes longer to compute.
The chain length determines how many computations you have to perform to recover a lost password if found in a chain.

The chain count is basically coverage. 
If you have more chains, assuming all else stays equal, you have better coverage. 
You can also get better coverage using longer chains, though, but then you're increasing time.

Then we sort using:
./rtsort .
This sorts all rainbow tables in the current directory.

Lastly, we will use the generated sorted rainbow table to crack:
./rcrack . -l ../salted6.txt

-l is used if the way we stored the hashes is in format of one-line-one-hash
.. is to backtrack one directory up.

The text file is in one directory above the rtcrack script and rainbow table
'''