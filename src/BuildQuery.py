import struct
import random


def buildQuery(domainName, qType):

    #Header Section
    ID = random.randint(0, (2**16) - 1) #randomly generates a unique ID for the query
    flags = 0x0100 #flags for a standard query
    QDCOUNT = 1
    ANCOUNT = 0
    NSCOUNT = 0
    ARCOUNT = 0

    # Packing the header fields into a binary string
    dnsHeader = struct.pack("!HHHHHH", ID, flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT)

    #convert domain name from string to the required (binary) format
    qName = b""
    for part in domainName.split("."):
        qName += bytes([len(part)]) + part.encode()
    qName += b"\x00"

    # Question Section
    queryType_dict = {"A": 0x0001, "NS": 0x0002, "MX": 0x000F}
    qType = queryType_dict.get(qType, 0x0001) #qtype defaults to A if its unkown (IS THIS RIGHT?)
    qClass = 0x0001 #internet class

    dnsQuestion = qName + struct.pack("!HH", qType, qClass)
    dnsQuery = dnsHeader + dnsQuestion

    return dnsQuery
