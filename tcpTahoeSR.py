class TCPRenoSender:
	def __init__(self, dataAmt, ipHeader, parentHost, destination, h):
		self.MSS = 1024.0
		self.isSource = True
		self.seq = 0
		self.ack = 0
		self.window = self.MSS
		self.ssThresh = self.MSS*10
		self.dupACKs = 0
		self.largestACK = 0
		self.largestSentPacket = 1
		self.ipHeader = ipHeader
		self.parentHost = parentHost
		self.destination = destination
		self.maxSeq = dataAmt
		self.state = 'Slow start'
		self.timeoutTime = float('inf')
		self.tcpFinished = False
		self.handler = h
		self.timeoutDelay = 1.0
	
	def doNext(self,action):
		if action == 'Check timeout' and not (self.state == 'Done'):
			t = self.handler.getTime()
			if self.timeoutTime <= t:
				self.timeout()
		
	def timeout(self):
		if self.state == 'Done':
			return
		else:
			self.ssThresh = self.window/2
			self.window = 1*self.MSS
			self.dupACKs = 0
			self.state = 'Slow start'
			putPacket(self.seq)
		
	def recvPacket(self,p):
		if self.state == 'Done':
			return
		elif self.state == 'Slow start':
			if p.tcpHeader.acknowledgeNumber <= self.largestACK:
				self.dupACKs += 1
				if self.dupACKs == 3:
					self.ssThresh = self.window/2
					self.window = 1*self.MSS
					retransmitMissingPacket()
					self.state = 'Slow start'
			elif p.tcpHeader.acknowledgeNumber*self.MSS >= maxSeq/1024:
				self.state = 'Done'
			else:
				self.window = self.window + self.MSS
				self.dupACKs = 0
				putPacket()
		elif self.state == 'Congestion avoidance':
			if p.tcpHeader.acknowledgeNumber <= self.largestACK:
				self.dupACKs += 1
				if self.dupACKs == 3:
					self.ssThresh = self.window/2
					self.window = self.MSS
					retransmitMissingPacket()
					self.state = 'Slow start'
			else:
				self.window = self.window+self.MSS*(self.MSS/self.window)
				self.dupACKs = 0
				putPacket()
				
	def putPacket(self,seq):
		tcpHeader = TCPHeader(seq,self.ack,self.window)
		ipHeader = self.ipHeader
		p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost,self.parentHost)
		self.parentHost.queue.append(p)
		self.largestPacketSent = seq*1024
				
	def generatePackets(self):
		for i in range(largestPacketSent/1024,(largestPacketSent + self.window)/1024):
			putPacket(i)
		heappush(eventQueue, (self.timeoutTime, self, 'checkTimeout') )
		self.parentHost.beginTransmit()
		self.seq = i
			
class TCPTahoeReceiver:
	def __init__(self, size, ipHeader, parentHost, destination):
		self.isSource = False
		self.seq = 0
		self.ack = 0
		self.windowStart = 1
		for i in range(2**14):
			self.windowList.append(0)
		self.ipHeader = ipHeader
		self.lasSeqReceived = 0
		self.parentHost = parentHost
		self.recvTime = []
		self.recvPacketCount = 0
		self.destination = destination
		
	def recvPacket(self,p):
		i = p.tcpHeader.sequenceNumber - self.windowStart
		self.windowList[i] = 1
		need = 0
		for i in range(len(self.windowList)):
			if not self.windowList[i]:
				need = i
				break
		if need:
			ack = need + self.windowStart
			tcpHeader = TCPHeader(ack,ack,len(self.windowList))
			p = Packet(tcpHeader,self,ipHeader,64,self,parentHost,self,parentHost)
			self.parentHost.queue.append(p)
			self.parentHost.beginTransmit()
		
		
		
		