import socket
import ssl
import sys
import re
from collections import defaultdict

def checkWeb(web):
    try:
        scket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scket.settimeout(3)

        ssl_scket = ssl.wrap_socket(scket, cert_reqs=ssl.CERT_REQUIRED, ca_certs="/etc/ssl/certs/ca-certificates.crt")
        ssl_scket.connect((web, 443)) # 443 - HTTPS (Hypertext Transfer Protocol over SSL/TLS)
    except:
        return "Detect Failed!"

    return ssl_scket.cipher()

if __name__ == '__main__':
    cipherSuite = defaultdict(int) # https://docs.python.org/2/library/collections.html#collections.defaultdict

    webList = open('websites.txt', 'rb')
    for web in webList:
        web = web.rstrip()

        cipherInfo = checkWeb(web)

        if str(cipherInfo).find("Detect Failed!") == -1 and cipherInfo[0] != "":
            cipherSuite[cipherInfo[0]] += 1

    print cipherSuite, "\n"
    for k,v in cipherSuite.items():
        print k, v

    webList.close()