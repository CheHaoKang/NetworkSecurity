#!/usr/bin/env python

import re
import os
import sys
from subprocess import Popen, PIPE, STDOUT

if __name__ == '__main__':
    try:
	# filter out IPv4 DNS query
        reStringIPv4Req = '^.*?IP\s+([0-9a-zA-Z\.]+)\s+>\s+([0-9a-zA-Z\.]+).*?\s+A\?\s+([0-9a-zA-Z\.]+)\..*?'
	# filter out IPv6 DNS query
        reStringIPv6Req = '^.*?IP\s+([0-9a-zA-Z\.]+)\s+>\s+([0-9a-zA-Z\.]+).*?AAAA\?\s+([0-9a-zA-Z\.]+)\..*?'

	# filter out IPv4 DNS response
        reStringIPv4Resp = '^.*?IP\s+([0-9a-zA-Z\.]+)\s+>\s+([0-9a-zA-Z\.]+).*?\s+A\s+([0-9a-zA-Z\.]+)\s+.*?'
	# filter out IPv6 DNS response
        reStringIPv6Resp = '^.*?IP\s+([0-9a-zA-Z\.]+)\s+>\s+([0-9a-zA-Z\.]+).*?\s+AAAA\s+([0-9a-zA-Z\:]+)\s+.*?'

	# use "sudo tcpdump -l udp" to gather UDP packets
        p = Popen(["sudo", "tcpdump", "-l", "udp"], stdout=PIPE, stderr=STDOUT)

	# use regular expressions to filter out related information
        for line in iter(p.stdout.readline, b''):
            reobj = re.compile(reStringIPv4Req, re.IGNORECASE)
            m = reobj.finditer(line)
            for i in m:
                print ("++reStringIPv4Req+")
                print i.group(1), i.group(2), i.group(3)
                print ("---")

            reobj = re.compile(reStringIPv4Resp, re.IGNORECASE)
            m = reobj.finditer(line)
            for i in m:
                print ("++reStringIPv4Resp+")
                print i.group(1), i.group(2), i.group(3)
                print ("---")

            reobj = re.compile(reStringIPv6Req, re.IGNORECASE)
            m = reobj.finditer(line)
            for i in m:
                print ("++reStringIPv6Req+")
                print i.group(1), i.group(2), i.group(3)
                print ("---")

            reobj = re.compile(reStringIPv6Resp, re.IGNORECASE)
            m = reobj.finditer(line)
            for i in m:
                print ("++reStringIPv6Resp+")
                print i.group(1), i.group(2), i.group(3)
                print ("---")

            print line, "\n"
        p.wait()  # wait for the subprocess to exit
    except:
        print "Unexpected error:", sys.exc_info()[0]
