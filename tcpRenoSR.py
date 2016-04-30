from globals import *
from eventHandler import *
from packet import IPHeader, TCPHeader, Packet
from heapq import heappush

class TCPRenoSender:
	def __init__(self,dataAmt,ipHeader,parentHost,destination,h):
		self.isSource = 1
		self.seq = 0				#Smallest unACK'ed packet
		self.ack = 0				#Next packet needed
		self.window = 1				#Number of packets allowed unACK'ed
		self.ssthresh = 10			#Threshhold for exponential growth
		self.dupACK = 0				#Number of duplicate ACK's encountered
		self.largestACK = 0			#largest ACK received so far
		self.largestSentPacket = 1	#Largest packet sent yet
		self.ipHeader = ipHeader	#IP header determined from flow
		self.parentHost = parentHost#pointer to host which this is running on
		self.destination = destination
		self.maxSeq = dataAmt/1024
		self.rtt_seq_num = 0		#seq number that tracks RTT (for congestion avoidance )
		self.rtt_flag = False
		self.windowList = []
		self.windowList.append(1)
		self.timeoutDelay = 1.0		#seconds
		self.timeoutTime = float('inf')
		self.handler = h
		self.tcpFinished = 0

		self.sentTime = []


	def doNext(self,action):
		if action == 'check Timeout' and not self.tcpFinished:
			#print 'timeout occurred on',self.parentHost.name
			#print self.timeoutTime
			t = self.handler.getTime()
			if self.timeoutTime <= t:
				self.timeout()
		
	def timeout(self):
		self.ssthresh = self.window/2
		self.window = 1
		self.windowList.append(self.window)
		tcpHeader = TCPHeader(self.seq,self.ack,self.window)
		p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost,self.parentHost)
		self.parentHost.wipeQueue()
		self.parentHost.queue.append(p)
		self.timeoutTime = self.handler.getTime() + self.timeoutDelay
		heappush(eventQueue, (self.timeoutTime, self, 'check Timeout') )
		self.parentHost.beginTransmit()

	def recvPacket(self,p):
		#print self.parentHost.name,'received ack',p.tcpHeader.acknowledgeNumber
		#print self.parentHost.name,'RTT_NUM: ',self.rtt_seq_num
		if p.tcpHeader.acknowledgeNumber <= self.largestACK:
			self.dupACK += 1
			#print 'duplicate ack received'
			if self.dupACK == 3:
				self.fastRetransmit()
				
		elif p.tcpHeader.acknowledgeNumber > self.maxSeq:
			#print 'TCP done sending packets'
			self.parentHost.timeoutTime = float('inf')
			self.tcpFinished = 1
			
		else:
			self.dupACK = 0
			self.seq = p.tcpHeader.acknowledgeNumber
			self.largestACK = p.tcpHeader.acknowledgeNumber
			if self.rtt_seq_num <= p.tcpHeader.acknowledgeNumber-1:
				self.rtt_seq_num = 0
				self.rtt_flag = True
			if self.window < self.ssthresh:
				self.window = self.window + 1
			else:
				if self.rtt_flag == True:
					self.window = self.window + 1
					self.rtt_flag = False
			self.windowList.append(self.window)
				
			self.ssthresh = max(self.window,self.ssthresh)
			next = max(self.largestSentPacket+1,p.tcpHeader.acknowledgeNumber)
			
			if self.rtt_seq_num == 0:
				self.rtt_seq_num = next
			seq = 0
			for seq in range(next,self.seq + self.window):
				self.putPacket(seq)
			self.largestSentPacket = seq
			if p.tcpHeader.sequenceNumber > self.largestSentPacket:
				self.largestSentPacket = p.tcpHeader.sequenceNumber
			if seq:
				self.timeoutTime = self.handler.getTime() + self.timeoutDelay
				heappush(eventQueue, (self.timeoutTime, self, 'check Timeout') )
				self.parentHost.beginTransmit()
			
	def putPacket(self,seq):
		tcpHeader = TCPHeader(seq,self.ack,self.window)
		ipHeader = self.ipHeader
		p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost,self.parentHost)
		self.sentTime.append(globals.time)
		self.parentHost.queue.append(p)
			
	def fastRetransmit(self):
		#print self.parentHost.name, 'is fast retransmitting...'
		tcpHeader = TCPHeader(self.largestACK,self.ack,self.window)
		p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost,self.parentHost)
		self.parentHost.queue.append(p)
		self.largestSentPacket = max(p.tcpHeader.sequenceNumber,self.largestSentPacket) #might be something wrong with this line.
		self.timeoutTime = self.handler.getTime() + self.timeoutDelay
		heappush(eventQueue, (self.timeoutTime, self, 'check Timeout') )
		self.parentHost.beginTransmit()
		self.ssthresh = self.ssthresh/2
		self.window = self.window/2
		
class TCPRenoReceiver:
	def __init__(self,size,ipHeader,parentHost,destination):
		self.isSource = 0
		self.seq = 0
		self.ack = 0
		self.windowStart = 1
		self.windowList = []
		for i in range(2**18):
			self.windowList.append(0)
		self.ipHeader = ipHeader
		self.lastSeqReceived = 0	
		self.parentHost = parentHost
		self.recvTime = []			# stores the time when packet has been received (for graphing purposes)
		self.recvPacketCount = 0
		self.destination = destination
		windowSizeList = []

	def recvPacket(self,p):
		#print self.parentHost.name,'received packet ',p.tcpHeader.sequenceNumber

		# Log packet receive time 
		self.recvTime.append(globals.time)


		i = p.tcpHeader.sequenceNumber - self.windowStart
		self.windowList[i] = 1
		need = 0
		for i in range(len(self.windowList)):
			if not self.windowList[i]:
				need = i
				break

		if need:
			ack = need + self.windowStart
			#print 'receiver is creating ack',ack
			tcpHeader = TCPHeader(ack,ack,len(self.windowList))
			p = Packet(tcpHeader,self.ipHeader,64,self.parentHost,self.parentHost)
			self.parentHost.queue.append(p)
			self.parentHost.beginTransmit()
		else:
			print 'out of room in window'