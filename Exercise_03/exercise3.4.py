#!/usr/bin/env python

import re
import os
import sys
import random
import hashlib
from subprocess import Popen, PIPE, STDOUT

FLAG_1 = 0b1111
FLAG_2 = 0b11111111
FLAG_3 = 0b111111111111

# use SHA256 to check bit coincidence. "numOfBits" identifies how many bits must be the same.
def checkSame(seq1, seq2, numOfBits):
    for i in xrange(numOfBits/4):
        if (int(hashlib.sha256(seq1).hexdigest()[i], 16) & FLAG_1) != \
            (int(hashlib.sha256(seq2).hexdigest()[i], 16) & FLAG_1):
            return False

    return True

if __name__ == '__main__':
    # Open a file for saving all used sequences
    dataFile = open("exercise3_4_data.txt", "wb")

    # a dictionary for storing counters for 4, 8, 12, 16 and 20 bits
    allCounter = dict()
    allCounter[4] = []
    allCounter[8] = []
    allCounter[12] = []
    allCounter[16] = []
    allCounter[20] = []

    # we run this collision programming 10 times for 4, 8, 12, 16 and 20 bits
    for times in xrange(10):
        counter = dict()
        counter[4] = 0
        counter[8] = 0
        counter[12] = 0
        counter[16] = 0
        counter[20] = 0

        # this list is used to record which one doesn't find the collision yet
        bitsList = [4, 8, 12, 16, 20]

        # This counter is used to record how many times for a prefix to find a collision
        counterRun = 0
        going = True
        while going:
            counterRun += 1
            # Generate random sequences
            randomSequence1 = open("/dev/urandom", "rb").read(64)
            randomSequence2 = open("/dev/urandom", "rb").read(64)

	    	dataFile.write("===Sequence 1===\n")
        	dataFile.write(randomSequence1 + "\n")
	    	dataFile.write("===Sequence 2===\n")
        	dataFile.write(randomSequence2 + "\n\n")

            deletedBits = []
            # Iterate through each prefix
            for i in bitsList:
                # Check if certain prefixes have collisions
                if counter[i] == 0 and checkSame(randomSequence1, randomSequence2, i):
                    print "Collision of", i, "bits:", counterRun
                    counter[i] = counterRun
                    deletedBits.append(i)
                    print (hashlib.sha256(randomSequence1).hexdigest())
                    print (hashlib.sha256(randomSequence2).hexdigest() + "\n")

            # Remove prefixes which alreay got collisions
            for bits in deletedBits:
                bitsList.remove(bits)

            if not bitsList:
                going = False

        print counter

        # Print out all collision information
        for bits in xrange(4, 24, 4):
            allCounter[bits].append(counter[bits])

    print allCounter

    dataFile.close()