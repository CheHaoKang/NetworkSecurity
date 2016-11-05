import os
import socket
import sys

def generateOneTimePad():
    global oneTimePadList

    # use /dev/urandom to generate random numbers
    oneTimePad = open("/dev/urandom", "rb").read(100)
    oneTimePadFile = open("oneTimePad.txt", "w+")

    oneTimePadList = list(oneTimePad)
    for i in xrange(len(oneTimePadList)):
    	# a random number modulo 26
        oneTimePadList[i] = ord(oneTimePadList[i]) % 26
        # put it into a file
        oneTimePadFile.write(str(oneTimePadList[i]) + "\n")

    oneTimePadFile.close()

def encryptMessage(msg):
    global modLetterMapping
    encryptedMessage = []

    msg = msg.upper()
    for i in xrange(len(msg)):
    	# encrypt a message by the one-time pad
        encryptedMessage.append(modLetterMapping[((ord(msg[i]) - ord('A')) + oneTimePadList[i]) % 26])

    encryptedMessage = "".join(encryptedMessage)
    return encryptedMessage

def decryptMessage(msg):
    global modLetterMapping
    decryptedMessage = []

    msg = msg.upper()
    for i in xrange(len(msg)):
    	# decrypt a message by the one-time pad
        decryptedMessage.append(modLetterMapping[((ord(msg[i]) - ord('A')) - oneTimePadList[i]) % 26])

    decryptedMessage = "".join(decryptedMessage)
    return decryptedMessage


if __name__ == "__main__":
    oneTimePadList = []
    modLetterMapping = {}

    # Create the mapping table of modulos and English letters
    # {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 
    # 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 
    # 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
    for i in xrange(26):
        modLetterMapping[i] = chr(ord('A') + i)

	# If oneTimePad.txt doesn't exist, generate it!
    if not os.path.exists("oneTimePad.txt"):
        generateOneTimePad()
    else:
        oneTimePadFile = open("oneTimePad.txt", "r")
        for line in oneTimePadFile:
            oneTimePadList.append(int(line.strip()))


    host, port = "localhost", 1234

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((host, port))
        sock.sendall("\n")

        # Receive data from the server and shut down
        f = sock.makefile()
        for l in f.readlines():
            print "Client received an encrypted message:", l
            print "Client decrypted the message to:", decryptMessage(l), "\n"
    finally:
        sock.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server and send data
        sock.connect((host, port))
        encryptedMessage = encryptMessage("OKIAMYOURCLIENT")
        print "Client encrypted \"OKIAMYOURCLIENT\" and sent \"" + encryptedMessage + "\" to the server"
        sock.sendall(encryptedMessage + "\n")
    finally:
        sock.close()