from globals import *
from eventHandler import *
import heapq

class Link:
	def __init__(self,name,rate,delay,buffer,c1,c2,h):
		self.name = name
		self.rate = rate*1e6/8.0			#convert to rate in MBps
		self.delay = delay/1000.0		#convert to seconds
		self.bufferSize = buffer*1000.0 #convert to bytes
		self.connection1 = c1			#c1 and c2 should be references
		self.connection2 = c2			#to the proper connected objects.
		c1.link.append(self)
		c2.link.append(self)
		self.handler = h
		
		self.bufferBytes = 0
		self.bufferFull = 0
		self.queue = []
		
		linkList.append(self)
		
	def recvPacket(self,p):
		time = self.handler.getTime()
		if self.bufferBytes < self.bufferSize:
			self.queue.append(p)
			self.bufferBytes = self.bufferBytes + p.size
			rateDelay = self.bufferBytes / self.rate
			heapq.heappush(eventQueue,(time + self.delay + rateDelay, self))
		else:
			print 'dropped packet',p.tcpHeader.sequenceNumber
	
	def sendPacket(self,p):
		if p.sender == self.connection1:
			self.connection2.recvPacket(p)
		elif p.sender == self.connection2:
			self.connection1.recvPacket(p)
		else:
			print 'ERROR ADDRESS DOES NOT MATCH EITHER CONNECTION'
			
		self.bufferBytes = self.bufferBytes - p.size

	def doNext(self):
		p = self.queue.pop(0)
		self.sendPacket(p)