import base64
import telnetlib
from time import sleep
import re
import sys
import math
import hashlib

def processMessage(message):
    global prime, generator, publicValDiffieX, publicValHellmanY, fakeKeyZ, sharedSecretKeyDiffie, sharedSecretKeyHellman, \
        sha512SharedSecretKeyDiffie, sha512SharedSecretKeyHellman

    # Use regular expression to extract messages we want
    re_primeGenerator = '.*Is the prime ([0-9]+) and the generator ([0-9]+) okay for you?'
    re_publicValueDiffie = '.*My public value would be ([0-9]+) then'
    re_publicValueHellman = '.*I computed mine to be ([0-9]+)!'


    reobj = re.compile(re_primeGenerator, re.IGNORECASE)
    m = reobj.finditer(message)
    for i in m:
        if i.group(1) != "":
            # get the prime
            prime = long(i.group(1))
            print "### Prime:", prime, "###"

        if i.group(2) != "":
            # get the generator
            generator = long(i.group(2))
            print "### Generator:", generator, "###"

            return message


    reobj = re.compile(re_publicValueDiffie, re.IGNORECASE)
    m = reobj.finditer(message)
    for i in m:
        if i.group(1) != "":
            publicValDiffieX = long(i.group(1))
            print "### Public value Diffie:", publicValDiffieX, "###"

            fakePublicValueZ = long(math.pow(generator, fakeKeyZ) % prime)
            print "### fakePublicValueZ:", fakePublicValueZ, "###"
            # substitute our fake public value for Diffie's public value
            message = re.sub(str(publicValDiffieX), str(fakePublicValueZ), message)
            print "### CHANGED MESSAGE:", message, "###"
            # Calculate Diffie's shared secret key
            sharedSecretKeyDiffie = long(publicValDiffieX % prime)
            print "### sharedSecretKeyDiffie", sharedSecretKeyDiffie, "###"
            sha512SharedSecretKeyDiffie = hashlib.sha512(str(sharedSecretKeyDiffie)).hexdigest()
            print "### sha512SharedSecretKeyDiffie", sha512SharedSecretKeyDiffie, "###"
            
            return message


    reobj = re.compile(re_publicValueHellman, re.IGNORECASE)
    m = reobj.finditer(message)
    for i in m:
        if i.group(1) != "":
            publicValHellmanY = long(i.group(1))
            print "### Public value Hellman:", publicValHellmanY, "###"

            fakePublicValueZ = long(math.pow(generator, fakeKeyZ) % prime)
            print "### fakePublicValueZ:", fakePublicValueZ, "###"
            # substitute our fake public value for Hellman's public value
            message = re.sub(str(publicValHellmanY), str(fakePublicValueZ), message)
            print "### CHANGED MESSAGE:", message, "###"
            # Calculate Hellman's shared secret key
            sharedSecretKeyHellman = long(publicValHellmanY % prime)
            print "### sharedSecretKeyHellman", sharedSecretKeyHellman, "###"
            sha512SharedSecretKeyHellman = hashlib.sha512(str(sharedSecretKeyHellman)).hexdigest()
            print "### sha512SharedSecretKeyHellman", sha512SharedSecretKeyHellman, "###"
            return message

    return message

def decryptMessage(message, diffieOrHellman):
    # use b64decode to decrypt the message
    decodedBase64 = base64.b64decode(message)

    if diffieOrHellman=="diffie":
        sha512 = sha512SharedSecretKeyDiffie
    else:
        sha512 = sha512SharedSecretKeyHellman

    decodedBase64List = list(decodedBase64)
    for i in xrange(len(decodedBase64List)):
        # print "### decodedBase64List[i]:", decodedBase64List[i], "###"
        # print "### ord(decodedBase64List[i]):", ord(decodedBase64List[i]), "###"
        # print "### sha512[i]:", sha512[i], "###"
        # print "### ord(sha512[i]):", ord(sha512[i]), "###"
        # print "### int(sha512[i], 16):", int(sha512[i], 16), "###"
        # print "### ord(decodedBase64List[i]) ^ int(sha512[i], 16):", ord(decodedBase64List[i]) ^ int(sha512[i], 16), "###"
        # print "### chr(ord(decodedBase64List[i]) ^ int(sha512[i], 16)):", chr(ord(decodedBase64List[i]) ^ int(sha512[i], 16)), "###"
        # print "### chr(ord(decodedBase64List[i]) ^ ord(sha512[i])):", chr(ord(decodedBase64List[i]) ^ ord(sha512[i])), "###\n"
        #decodedBase64List[i] = chr(ord(decodedBase64List[i]) ^ int(sha512[i], 16))
        # Use XOR to get the original message
        decodedBase64List[i] = chr(ord(decodedBase64List[i]) ^ ord(sha512[i]))
        # print "### decodedBase64", decodedBase64

    return ''.join(decodedBase64List)


def encryptMessage(message, diffieOrHellman):
    if diffieOrHellman=="diffie":
        sha512 = sha512SharedSecretKeyDiffie
    else:
        sha512 = sha512SharedSecretKeyHellman

    messageList = list(message)
    for i in xrange(len(messageList)):
        # XOR the original message
        messageList[i] = chr(ord(messageList[i]) ^ ord(sha512[i]))

    message = ''.join(messageList)

    # Use b4encode to encode the message
    return base64.b64encode(message)


if __name__ == '__main__':
    prime = 7
    generator = 3
    publicValDiffieX = -1
    publicValHellmanY = -1
    fakeKeyZ = 1
    sharedSecretKeyDiffie = -1
    sha512SharedSecretKeyDiffie = -1
    sharedSecretKeyHellman = -1
    sha512SharedSecretKeyHellman = -1

    diffie = telnetlib.Telnet("10.0.0.12", 3333)
    hellman = telnetlib.Telnet("10.0.0.12", 4444)

    startCom = False
    messageDiffie = []
    messageHellman = []

    # Use a while loop to read messages from Diffie and Hellman
    try:
        while True:
            # Diffie Part
            message = diffie.read_until('\n', 0.20).rstrip()
            print "\n>>> Read from DIFFIE:", message, "###"
            if message != "":
                if startCom == True:
                    messageDiffie.append(message.rstrip())
                    # decrypt Diffie's message
                    message = decryptMessage(message, "diffie")
                    print "###", message, "###"
                    # encrypt with Hellman's key
                    message = encryptMessage(message, "hellman")

                if startCom == False and message.find("SHA512") != -1:
                    #print "### ", message.find("SHA512")
                    print "\n\n### Start communicating ###"
                    # From here, Diffie and Hellman start to communicate with each other
                    startCom = True

                if startCom==False:
                    message = processMessage(message)
                    # print "### RETURNED MESSAGE:", message, "###"

                # print "### BEFORE hellman.write(message):", message, "###"
                hellman.write(message)
            #####

            # Hellman part
            message = hellman.read_until('\n', 0.20).rstrip()
            print "\n>>> Read from HELLMAN:", message, "###"
            if message != "":
                if startCom == True:
                    messageHellman.append(message.rstrip())
                    # decrypt Hellman's message
                    message = decryptMessage(message, "hellman")
                    print "###", message, "###"
                    # encrypt with Diffie's key
                    message = encryptMessage(message, "diffie")

                if startCom == False:
                    message = processMessage(message)
                    # print "### RETURNED MESSAGE:", message, "###"

                # print "### BEFORE diffie.write(message):", message, "###"
                diffie.write(message)
            #####
    except:
        print sys.exc_info()

    # print "### messageDiffie:", messageDiffie, "###"
    # print "### messageHellman:", messageHellman, "###"