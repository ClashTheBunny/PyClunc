#!/usr/bin/env python

# Copyright 2011 Randall Mason
# GPLv3 License

import binascii
import struct

lumpMACoffset = 2
eth_alen = 6
ipv4AddrSize = 4

lumpHeader = '4sI'
lumpMACField = lumpHeader + lumpHeader + str(lumpMACoffset + eth_alen) + 's'
lumpIPField = lumpHeader + lumpHeader + str(ipv4AddrSize) + 's'

lumpPacket = lumpHeader + lumpMACField*2 + lumpIPField

header = binascii.b2a_hex(struct.pack('!' + lumpHeader,'LUMP',struct.calcsize('!' + lumpPacket) - struct.calcsize('!' + lumpHeader)))

# Target MAC Address
targetMAC = '\x00\xd0\x4b\x8d\x32\xaa'
targetMACstring = binascii.b2a_hex(struct.pack('!' + lumpMACField ,'MACD', 16, 'MAC@',(lumpMACoffset + eth_alen),targetMAC))

# New MAC Address
newMAC = '\x00'*(lumpMACoffset + eth_alen)
newMACstring = binascii.b2a_hex(struct.pack('!' + lumpMACField ,'MACS', 16, 'MAC@',(lumpMACoffset + eth_alen),newMAC))

# New IP Address
newIP = '\x00'*ipv4AddrSize
newIPstring = binascii.b2a_hex(struct.pack('!' + lumpIPField ,'IPS', 12, 'IP@',ipv4AddrSize,newIP))

print header + targetMACstring + newMACstring + newIPstring
