from globals import *
import heapq

class IPHeader:
	def __init__(self,timeToLive,sourceAddress,destinationAddress):
		self.timeToLive = timeToLive
		self.sourceAddress = sourceAddress
		self.destinationAddress = destinationAddress
		
#The above are important to the simulation
#The following were left out because they are likely irrelevant
#Version, header length, TOS, total length, identification, flags,
#header checksum, fragment offset, protocol, options

class TCPHeader:
	def __init__(self,seq,ack,cwnd):
		self.sequenceNumber = seq
		self.acknowledgeNumber = ack
		self.windowSize = cwnd
		
#The above are important to the simulation
#The following were left out because they are likely irrelevent
#Data offset, Reserved, flags, urgent pointer, checksum, options,
#padding, Data

class Packet:
	def __init__(self,tcpHeader,ipHeader,size,immSender,origSender):
		self.tcpHeader 	= tcpHeader
		self.ipHeader 	= ipHeader
		self.immSender 	= immSender
		self.origSender = origSender
		self.size 		= size
		self.isDistancePacket = False;


class RouterPacket:
	def __init__(self, size, DSDV_data, sender):
		self.size = size;
		self.isDistancePacket = True;
		self.DSDV_data = DSDV_data;
		self.sender = sender;
		self.immSender = sender;


