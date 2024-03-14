import struct
from io import BytesIO

TYPE_A = 0x0001
TYPE_NS = 0x0002
TYPE_MX = 0x000F
TYPE_CNAME = 0x0005


def recordResponse(parser):
    parser = BytesIO(parser)  # Wrap the bytes object using BytesIO
    global header
    header = parseHeader(parser)
    question = parseQuestion(parser)
    records = []
    if header["anCount"] == 0:
        print("NOTFOUND")
    else:
        print(f"\n***Answer Section ({header['anCount']} records)***")
        for _ in range(header["anCount"]):
            record = parseRecord(parser)
            records.append(record)
            isAuth = "auth" if header["aa"] == 1 else "nonauth"
            printRecord(record, isAuth)

    if header["arCount"] > 0:
        print(f"\n***Additional Section ({header['arCount']} records)***")
        for _ in range(header["arCount"]):
            record = parseRecord(parser)
            records.append(record)
            isAuth = "auth" if header["aa"] == 1 else "nonauth"
            printRecord(record, isAuth)
    else:
        print(f"\n***Additional Section ({header['arCount']} records)***")
        print("NOTFOUND")

    return header, question, records


def printRecord(record, isAuth):
    # Determine the record type and construct the print string accordingly
    if record["ansType"] == TYPE_A:
        print(f"IP\t{record['rData']}\t{record['ttl']}\t{isAuth}")
    elif record["ansType"] == TYPE_CNAME:
        print(f"CNAME\t{record['rData']}\t{record['ttl']}\t{isAuth}")
    elif record["ansType"] == TYPE_MX:
        print(
            f"MX\t{record['rData']['exchange']}\t{record['rData']['preference']}\t{record['ttl']}\t{isAuth}"
        )
    elif record["ansType"] == TYPE_NS:
        print(f"NS\t{record['rData']}\t{record['ttl']}\t{isAuth}")
    else:
        print("could not resolve type")


def parseHeader(parser):
    id, flags, qdCount, anCount, nsCount, arCount = struct.unpack(
        "!6H", parser.read(2 * 6)
    )

    qr = (flags >> 15) & 1
    opCode = (flags >> 11) & 0xF
    aa = (flags >> 10) & 1
    tc = (flags >> 9) & 1
    rd = (flags >> 8) & 1
    ra = (flags >> 7) & 1
    z = (flags >> 4) & 7
    rCode = flags & 0xF

    headerDict = {
        "id": id,
        "qr": qr,
        "opCode": opCode,
        "aa": aa,
        "tc": tc,
        "rd": rd,
        "ra": ra,
        "z": z,
        "rCode": rCode,
        "qdCount": qdCount,
        "anCount": anCount,
        "nsCount": nsCount,
        "arCount": arCount,
    }
    return headerDict


def parseQuestion(parser):
    domainName = decodeDomainName(parser)
    qType, qClass = struct.unpack("!2H", parser.read(2 * 2))
    questionDict = {"domainName": domainName, "qType": qType, "qClass": qClass}
    return questionDict


def parseRecord(parser):
    global rData
    domainName = decodeDomainName(parser)
    ansType, ansClass, ttl, rdLength = struct.unpack(
        "!2HIH", parser.read(2 + 2 + 4 + 2)
    )

    if ansType == TYPE_A:
        rDataRaw = parser.read(rdLength)
        rData = ".".join([str(octet) for octet in rDataRaw])
    elif ansType == TYPE_NS:
        rData = decodeDomainName(parser)
    elif ansType == TYPE_CNAME:
        rData = decodeDomainName(parser)
    elif ansType == TYPE_MX:
        preference = parser.read(2)
        preference = struct.unpack("!H", preference)[0]
        exchange = decodeDomainName(parser)
        rData = {"preference": preference, "exchange": exchange}

    recordDict = {
        "domainName": domainName,
        "ansType": ansType,
        "ansClass": ansClass,
        "ttl": ttl,
        "rdLength": rdLength,
        "rData": rData,
    }
    return recordDict


def decodeDomainName(parser):
    domainNameParts = []
    while (nextLength := parser.read(1)[0]) != 0:
        if nextLength & 0b1100_0000 != 0:
            domainNameParts.append(decodeCompressedDomainName(nextLength, parser))
            break
        else:
            domainNameParts.append(parser.read(nextLength))
    domainName = b".".join(domainNameParts)
    return domainName


def decodeCompressedDomainName(nextLength, parser):
    pointerBytes = bytes([nextLength & 0b0011_1111]) + parser.read(1)
    pointer = struct.unpack("!H", pointerBytes)[0]
    currentPosition = parser.tell()
    parser.seek(pointer)
    result = decodeDomainName(parser)
    parser.seek(currentPosition)
    return result
