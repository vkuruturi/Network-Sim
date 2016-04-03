from globals import hostList,linkList,routerList,flowList,eventQueue,time
from tcpRenoSR import TCPRenoSender, TCPRenoReceiver
from packet import IPHeader, TCPHeader, Packet
from heapq import heappush

class Host:
	def __init__(self,name,ipAddress,algorithm,h):
		self.name = name
		self.ipAddress = ipAddress
		self.link = []
		self.queue = []
		hostList.append(self)
		self.tcpAlgorithm = algorithm	
		self.handler = h
		self.timer = 0
		
	def doNext(self):
		if self.handler.getTime() >= self.timer:
			self.tcp.timeout()
	
	def attemptTransmit(self):
		for i in range (len(self.queue) ):
			p = self.queue.pop(0)
			self.link[0].recvPacket(p)
		if self.sender:
			t = self.handler.getTime()
			self.timer = t + 2.0
			heappush(eventQueue,(t+2.0,self) )
		
			
	def initiateTCP(self,destination,size,srcPort,dstPort,sender):
		self.sender = sender
		if self.tcpAlgorithm == 'TCP Reno':
			if sender == 1:
				ipHeader = IPHeader(15,self.ipAddress,destination.ipAddress)
				self.tcp = TCPRenoSender(size,srcPort,dstPort,ipHeader,self)
				self.tcp.createPacketsInRange(1,2)
				self.attemptTransmit()
			elif sender == 0:
				ipHeader = IPHeader(15,self.ipAddress,destination.ipAddress)
				self.tcp = TCPRenoReceiver(0,srcPort,dstPort,ipHeader,self)
			else:
				print 'Error, not sender or receiver'
		else:
			print 'Error, not a valid TCP choice'

	def recvPacket(self,p):
		self.tcp.recvPacket(p)