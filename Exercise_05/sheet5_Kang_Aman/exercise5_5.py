#-*-coding:utf-8-*-
import re
import os
import hashlib
import sys
import binascii

if sys.version_info < (3, 6):
    import sha3

__author__ = 'Che-Hao Kang'
# name2key - 5847cc4e0a

if __name__ == "__main__":
    blockSize = 72          # block size of SHA3-512: 576 bits = 72 bytes
    name2Key = "5847cc4e0a" # as ASCII
    iPad = binascii.unhexlify("93")
    oPad = binascii.unhexlify("A5")

    # pad the key with leading zeros
    paddedName2Key = list(name2Key)
    for i in range(blockSize-len(paddedName2Key)):
         paddedName2Key = ['0'] + paddedName2Key
    paddedName2Key = ''.join(paddedName2Key)
    paddedName2Key = str.encode(paddedName2Key)

    # k ⊕ ipad
    xorIPad = b''
    for i in range(len(paddedName2Key)):
        xorIPad += bytes([paddedName2Key[i] ^ iPad[0]])

    # k ⊕ opad
    xorOPad = b''
    for i in range(len(paddedName2Key)):
        xorOPad += bytes([paddedName2Key[i] ^ oPad[0]])

    # generate the pdf file bytes
    pdfBytes = b''
    f = open("netsec2016_exercise_sheet_05.pdf", "rb")
    try:
        while True:
            b = f.read(1)
            if not b:
                break
            pdfBytes += b
    finally:
        f.close()

    # (k ⊕ ipad) || m
    xorIPadM = b''
    xorIPadM = xorIPad + pdfBytes

    # h( (k ⊕ ipad) || m ) with sha3_512
    hashXorIPadM = hashlib.sha3_512(xorIPadM).digest()

    # h(k ⊕ opad || h(k ⊕ ipad || m))
    hmac = hashlib.sha3_512(xorOPad + hashXorIPadM).digest()
    print ("hmac:{0}".format(hmac))