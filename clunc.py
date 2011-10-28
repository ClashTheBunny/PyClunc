#!/usr/bin/env python

# Copyright 2011 Randall Mason
# GPLv3 License

import binascii
import struct

import sys 
from socket import SOL_SOCKET, SO_BROADCAST 
import socket

from twisted.internet import reactor 
from twisted.internet import protocol 
from twisted.internet import task 
from twisted.python import log 

log.startLogging(sys.stdout) 
 
port = 7154 
 
class BroadcastingDatagramProtocol(protocol.DatagramProtocol): 
  port = port 
  def startProtocol(self): 
    self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True) 
    self.call = task.LoopingCall(self.tick) 
    self.dcall = self.call.start(1.0) 
  def stopProtocol(self): 
    self.call.stop() 
  def tick(self): 
    self.transport.write(self.getPacket(ip='192.168.1.3'), ("<broadcast>", self.port)) 
  def datagramReceived(self, data, addr): 
    print "Received", repr(data) 
  def getPacket(self,ip='\x00\x00\x00\x00',mac='\x00\x00\x00\x00\x00\x00'):
    lumpMACoffset = 2
    eth_alen = 6
    ipv4AddrSize = 4
    lumpHeader = '4sI'
    lumpMACField = lumpHeader + lumpHeader + str(lumpMACoffset + eth_alen) + 's'
    lumpIPField = lumpHeader + lumpHeader + str(ipv4AddrSize) + 's'
    lumpPacket = lumpHeader + lumpMACField*2 + lumpIPField
    header = struct.pack('!' + lumpHeader,'LUMP',struct.calcsize('!' + lumpPacket) - struct.calcsize('!' + lumpHeader))
    # Target MAC Address
    targetMAC = mac
    targetMAC = struct.pack('!' + lumpMACField ,'MACD', 16, 'MAC@',(lumpMACoffset + eth_alen),'\x00'*lumpMACoffset + targetMAC)
    # New MAC Address
    newMAC = '\x00'*(lumpMACoffset + eth_alen) # set to zeros to not use; always zero in clunc
    newMAC = struct.pack('!' + lumpMACField ,'MACS', 16, 'MAC@',(lumpMACoffset + eth_alen), '\x00'*lumpMACoffset + newMAC)
    # New IP Address
    newIP = socket.inet_aton(ip)
    newIP = struct.pack('!' + lumpIPField ,'IPS', 12, 'IP@',ipv4AddrSize,newIP)
    return header + targetMAC + newMAC + newIP

reactor.listenUDP(port, BroadcastingDatagramProtocol()) 
reactor.run()
