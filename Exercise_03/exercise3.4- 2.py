#!/usr/bin/env python

import re
import os
import sys
import random
import hashlib
from subprocess import Popen, PIPE, STDOUT
#from contextlib import redirect_stdout

FLAG_1 = 0b1111
FLAG_2 = 0b11111111
FLAG_3 = 0b111111111111

def checkSame(seq1, seq2, numOfBits):
    for i in xrange(numOfBits/4):
        if (int(hashlib.sha256(seq1).hexdigest()[i], 16) & FLAG_1) != \
            (int(hashlib.sha256(seq2).hexdigest()[i], 16) & FLAG_1):
            return False

    return True

if __name__ == '__main__':
    # print FLAG_1
    # randomSequence1 = open("/dev/urandom", "rb").read(1)
    # randomSequence1 = "$"
    # randomSequence2 = "f"
    # print randomSequence1
    # # print randomSequence2
    # print hashlib.sha256(randomSequence1).hexdigest()
    # # print hashlib.sha256(randomSequence2).hexdigest()
    # a = hashlib.sha256(randomSequence1).hexdigest()[2]
    # print bin(int(a, 16))
    # print int(a, 16) & FLAG_1
    #print int(hashlib.sha256(randomSequence1).hexdigest()[2]) & 11110000
    # print hashlib.sha256(randomSequence2).hexdigest()
    # print hashlib.sha256(randomSequence2).hexdigest()[1]

    # Open a file
    dataFile = open("exercise3_4_data.txt", "wb")

    allCounter = dict()
    allCounter[4] = []
    allCounter[8] = []
    allCounter[12] = []
    allCounter[16] = []
    allCounter[20] = []

    for times in xrange(2):
        counter = dict()
        counter[4] = 0
        counter[8] = 0
        counter[12] = 0
        counter[16] = 0
        counter[20] = 0

        bitsList = [4, 8, 12, 16, 20]

        counterRun = 0
        going = True
        while going:
            counterRun += 1
            randomSequence1 = open("/dev/urandom", "rb").read(64)
            randomSequence2 = open("/dev/urandom", "rb").read(64)

	    dataFile.write("===Sequence 1===\n")
            dataFile.write(randomSequence1 + "\n")
	    dataFile.write("===Sequence 2===\n")
            dataFile.write(randomSequence2 + "\n\n")

            # print ("randomSequence1:", randomSequence1)
            # print ("randomSequence2:", randomSequence2)

            deletedBits = []
            for i in bitsList:
                # print i
                if counter[i] == 0 and checkSame(randomSequence1, randomSequence2, i):
                    print "Collision of", i, "bits:", counterRun
                    counter[i] = counterRun
                    deletedBits.append(i)
                    print (hashlib.sha256(randomSequence1).hexdigest())
                    print (hashlib.sha256(randomSequence2).hexdigest() + "\n")

            # print ("================================")

            for bits in deletedBits:
                bitsList.remove(bits)

            if not bitsList:
                going = False

        print counter

        for bits in xrange(4, 24, 4):
            allCounter[bits].append(counter[bits])

    print allCounter

    # Close opend file
    dataFile.close()
    # print (randomSequence1)
    # print (hashlib.sha256(randomSequence1).digest())
    # print (hashlib.sha256(randomSequence1).hexdigest())
    #print (os.urandom(4))
    #buf = '\x00' + ''.join(chr(random.randint(0, 255)) for _ in range(0)) + '\x00'
    #print (buf)
