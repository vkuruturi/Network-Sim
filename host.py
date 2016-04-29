from globals import hostList,linkList,routerList,flowList,eventQueue,time
from tcpRenoSR import TCPRenoSender, TCPRenoReceiver
from packet import IPHeader, TCPHeader, Packet
from heapq import heappush

class Host:
	def __init__(self, name, ipAddress, algorithm, h):
		self.name = name				#string identifer of object
		self.tcpAlgorithm = algorithm	#algoritm string
		self.ipAddress = ipAddress		#for routing algoritms
		self.handler = h				#global time keeper
		self.queue = []					#list of packets ready to be sent
		self.tcp = []					#list of tcp connections
		self.handler = h
		self.initialized = 1;
		self.handler.getHostList().append(self);
		self.isRouter = 0;
		
	def setLink(self,link):				#set link connection
		self.link = link

	def wipeQueue(self):
		self.queue = []
		
	def doNext(self,action):
		if action == 'push':
			if len(self.queue):
				p = self.queue.pop(0)
				print 'Host',self.name,'is attempting to push packet',p.tcpHeader.sequenceNumber
				self.link.recvPacket(p)
				if len(self.queue) >= 1:
					print 'Host',self.name,'transmitting again'
					self.beginTransmit()
				else:
					print 'Host',self.name,'ending transmission'
					return
			else:
				print 'Nothing in queue, cannot push'
	
	def beginTransmit(self):						#begin transmitting next packet in queue
		t = self.handler.getTime()					#set the time
		p = self.queue[0]							#look at next packet
		ttp = t + (p.size/self.link.rate)			#time to push to link
		heappush(eventQueue, (ttp, self, 'push'))
		
	def findTCP(self,destination,isSource):
		for i in range( len(self.tcp) ):							#loop through all TCP's
			if self.tcp[i].destination == destination and self.tcp[i].isSource == isSource:	#if one has a matching destination and source
				return self.tcp[i]						#return it
		print 'Error no TCP connection has that destination'
	def sendDSDV(self):
		swag = "Sahil"
			
	def initiateTCP(self, destination, size, isSource, flow):
		print self.name,'is initializing tcp, isSource =',isSource
		print 'destination is',destination.name
		self.isSource = isSource							#isSource is a bool indicating flow source
		if self.tcpAlgorithm == 'TCP Reno':
			if isSource == 1:
				maxHops = 15 								#this may be changed to some variable
				ipHeader = IPHeader(maxHops, self.ipAddress, destination.ipAddress)	#create IP header
				self.tcp.append( TCPRenoSender(size, ipHeader, self, destination, self.handler) )	#creates a new TCP connection
				tempTCP = self.findTCP(destination,isSource)
				flow.srcTCP = tempTCP
				tempTCP.timeoutTime = self.handler.getTime() + tempTCP.timeoutDelay
				heappush(eventQueue, (tempTCP.timeoutTime, tempTCP, 'checkTimeout') )
				tempTCP.putPacket(1)								#find TCP corresponding to destination
				self.beginTransmit()											
			elif isSource == 0:
				ipHeader = IPHeader(15,self.ipAddress,destination.ipAddress)		#for the case of the receiver:
				self.tcp.append(TCPRenoReceiver(0, ipHeader,self,destination))
				tempTCP = self.findTCP(destination,isSource)
				flow.dstTCP = tempTCP
			else:
				print 'Error, not sender or receiver'
		elif self.tcpAlgorithm == 'TCP Tahoe':
			if isSource == 1:
				maxHops = 15 								#this may be changed to some variable
				ipHeader = IPHeader(maxHops, self.ipAddress, destination.ipAddress)	#create IP header
				self.tcp.append( TCPRenoSender(size, ipHeader, self, destination, self.handler) )	#creates a new TCP connection
				tempTCP = self.findTCP(destination,isSource)
				flow.srcTCP = tempTCP
				tempTCP.timeoutTime = self.handler.getTime() + tempTCP.timeoutDelay
				heappush(eventQueue, (tempTCP.timeoutTime, tempTCP, 'checkTimeout') )
				tempTCP.putPacket(1)								#find TCP corresponding to destination
				self.beginTransmit()
			elif isSource == 0:
				ipHeader = IPHeader(15,self.ipAddress,destination.ipAddress)		#for the case of the receiver:
				self.tcp.append(TCPRenoReceiver(0, ipHeader,self,destination))
				tempTCP = self.findTCP(destination,isSource)
				flow.dstTCP = tempTCP
			else:
				print 'Error, not sender or reciever'

		else:
			print 'Error, not a valid TCP choice'

	def recvPacket(self,p):
		if p.size == 64:
			self.findTCP(p.origSender,1).recvPacket(p)
		if p.size == 1024:
			self.findTCP(p.origSender,0).recvPacket(p)