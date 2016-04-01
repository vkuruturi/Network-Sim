from globals import *
from eventHandler import *
from packet import IPHeader, TCPHeader, Packet
from heapq import heappush

class TCPRenoSender:
	def __init__(self,dataAmt,srcPort,dstPort,ipHeader,parentHost):
		self.seq = 0				#Smallest unACK'ed packet
		self.ack = 0				#Next packet needed
		self.bytesToSend = dataAmt	#Total amount of MebiBytes to transfer
		self.window = 1				#Number of packets allowed unACK'ed
		self.ssthresh = 20		#Threshhold for exponential growth
		self.dupACK = 0				#Number of duplicate ACK's encountered
		self.srcPort = srcPort		#TCP source port, mostly irrelevent
		self.dstPort = dstPort		#similar to above
		self.largestACK = 0			#largest ACK received so far
		self.largestSentPacket = 1	#Largest packet sent yet
		self.ipHeader = ipHeader	#IP header determined from flow
		self.parentHost = parentHost#pointer to host which this is running on
		self.windowList = []		#Vector to store window sizes over time
		self.maxSeq = self.bytesToSend/1024
		
	def timeout(self):
		self.ssthresh = self.window/2
		self.window = 1
		tcpHeader = TCPHeader(self.srcPort,self.dstPort,self.seq,self.ack,self.window)
		p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost)
		self.parentHost.queue = []
		self.parentHost.queue.append(p)
		self.parentHost.attemptTransmit()
		
	def createPacketsInRange(self,start,end):	#clearly the range exludes end
		end = min(end,self.maxSeq)
		for seq in range(start,end):
		
			print self.parentHost.name,'TCP created a packet with sequence number',seq
			
			tcpHeader = TCPHeader(self.srcPort,self.dstPort,seq,self.ack,self.window)
			ipHeader = self.ipHeader
			p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost)
			self.parentHost.queue.append(p)
			
			if p.tcpHeader.sequenceNumber > self.largestSentPacket:
				self.largestSentPacket = p.tcpHeader.sequenceNumber
		
	def recvPacket(self,p):
		
		print self.parentHost.name,'received ack',p.tcpHeader.acknowledgeNumber
		
		if p.tcpHeader.acknowledgeNumber == self.largestACK:
			print self.parentHost.name,'received duplicate ACK ',self.largestACK
			
			self.dupACK += 1
			if self.dupACK == 3:
				self.fastRetransmit()
				
		elif p.tcpHeader.acknowledgeNumber > self.maxSeq:
			print 'TCP done sending packets'
			self.parentHost.timer = float('inf')
			self.parentHost.queue = []
			print self.windowList
		else:
			self.dupACK = 0
			self.seq = p.tcpHeader.acknowledgeNumber
			self.largestACK = p.tcpHeader.acknowledgeNumber
			if self.window < self.ssthresh:
				self.window = 2*self.window
			else:
				self.window = self.window + 1
				
			self.ssthresh = max(self.window,self.ssthresh)

			self.windowList.append(self.window)
			nex = max(self.largestSentPacket+1,p.tcpHeader.acknowledgeNumber)
			self.createPacketsInRange(nex,self.seq+self.window)
			self.parentHost.attemptTransmit()
			
	def fastRetransmit(self):
		print self.parentHost.name, 'is fast retransmitting...'
		tcpHeader = TCPHeader(self.srcPort,self.dstPort,self.largestACK,self.ack,self.window)
		p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost)
		self.parentHost.queue.append(p)
		self.largestSentPacket = max(p.tcpHeader.sequenceNumber,self.largestSentPacket)
		self.parentHost.attemptTransmit()
		self.ssthresh = self.ssthresh/2
		self.window = self.window/2
		
		#Must implement fast recover
		
class TCPRenoReceiver:
	def __init__(self,dataAmt,srcPort,dstPort,ipHeader,parentHost):
		self.seq = 0
		self.ack = 0
		self.windowStart = 1
		self.windowList = []
		for i in range(2**11):
			self.windowList.append(0)
		self.srcPort = srcPort
		self.dstPort = dstPort
		self.ipHeader = ipHeader
		self.lastSeqReceived = 0	
		self.parentHost = parentHost
		
	def recvPacket(self,p):
		print self.parentHost.name,'received packet ',p.tcpHeader.sequenceNumber
		
		i = p.tcpHeader.sequenceNumber - self.windowStart
		self.windowList[i] = 1
		need = 0
		for i in range(len(self.windowList)):
			if not self.windowList[i]:
				need = i
				break
		if need:
			ack = need + self.windowStart
			print 'receiver is creating ack',ack
			tcpHeader = TCPHeader(self.srcPort,self.dstPort,0,ack,len(self.windowList))
			p = Packet(tcpHeader,self.ipHeader,64,self.parentHost)
			self.parentHost.queue.append(p)
			self.parentHost.attemptTransmit()
		else:
			print 'out of room in window'