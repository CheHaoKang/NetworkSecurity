#!/usr/bin/env python

import re
import os

if __name__ == '__main__':
    strings = []
    salt = "/pE9u4cQ" # Assign the salt for generating MD5 passwords
    answer = "$apr1$/pE9u4cQ$ZfQfXfZ8NWh2gfFpIx22T0" # The wanted answer

    # Read the document and save every word into a list
    with open('rfc3093.txt') as iF:
        for line in iF:
            lineSplit = line.strip().split()
            for ele in lineSplit:
                strings.append(ele)

    for ele in strings:
        # Only keep English words and eliminate all the others
        word = re.sub("[^A-Za-z]", "", ele)

        if word == "":
            continue

        try:
            while True:
                # employ Linux command to generate MD5 passwords
                f = os.popen("openssl passwd -apr1 -salt " + salt + " " + word)
                result = f.read().strip()

                if result != "":
                    print "result:", result
                    break
        except:
            print "os.popen FAILED!"

        # A go!
        if result == answer:
            print "\n\nGOT IT:", ele, result
            break