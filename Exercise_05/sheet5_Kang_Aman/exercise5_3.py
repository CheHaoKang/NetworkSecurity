import re
import os
import hashlib
import sys
import binascii

# Authenticator: 20baa7d33f8a6a887e2e955cf037ee6f
# User-Password (encrypted): cd26025db01442cb4e7ec72f9819a825

if __name__ == '__main__':
    strings = []
    # transform request authenticator to bytes
    requestAuth = binascii.unhexlify("20baa7d33f8a6a887e2e955cf037ee6f")
    # transform RADIUS User-Password Attribute to bytes
    userPasswordAttr = binascii.unhexlify("cd26025db01442cb4e7ec72f9819a825")

    print ("requestAuth:{0}   userPasswordAttr:{1}".format(requestAuth, userPasswordAttr))

    # read password from password.txt
    with open("password.txt") as pw:
        password = pw.readline()

    # pad the password with zeros at the end until it has 16 bytes
    password = str.encode(password.ljust(16, '0'))

    # Read the document and save every word into a list
    with open('rfc7511.txt') as iF:
        for line in iF:
            lineSplit = line.strip().split()
            for ele in lineSplit:
                strings.append(ele)

    for word in strings:
        try:
            print ("###" + word + "###")

            # transform an RFC-7511 word to bytes
            bytesWord = str.encode(word)
            print("bytesWord:###{0}###".format(bytesWord))

            # append bytesWord with request authenticator <= (K || RA)
            appendByte = bytesWord + requestAuth
            print ("### appendByte: ###{0}###".format(appendByte))

            # generate MD5 of appendByte <=  MD5 (K || RA)
            md5 = hashlib.md5(appendByte).digest()
            print ("### MD5:###{0}###".format(md5))
            print ("###len:{0} password: ###{1}###:".format(len(password), password))

            # set xorResult to bytes <= MD5(K || RA) ⊕ UP
            xorResult = b''
            print ("md5 len:{0}  reqAuth len:{1}  userAttr len:{2}".format(len(md5), len(requestAuth), len(userPasswordAttr)))
            for i in range(len(md5)):
                print ("md5[i] ^ password[i]:", md5[i] ^ password[i])
                print ("bytes([md5[i] ^ password[i]]):", bytes([md5[i] ^ password[i]]))
                xorResult += (bytes([md5[i] ^ password[i]]))
            print ("xorResult len:{0}    xorResult:{1}".format(len(xorResult), xorResult))
            print ("{0}\n".format(userPasswordAttr))

            if xorResult == userPasswordAttr:
                 print ("The shared secret is =>", word)
                 break
        except:
            print (sys.exc_info())
