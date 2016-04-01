from globals import *
import heapq

class Flow:
	def __init__(self,name,source,destination,amount,start,algo,srcPort,dstPort,h):
		self.name = name
		self.source = source
		self.destination = destination
		self.dataAmount = amount
		self.startTime = start
		self.Algorithm = algo
		self.srcPort = srcPort
		self.dstPort = dstPort
		
		flowList.append(self)
		heapq.heappush(eventQueue,(self.startTime,self))
		
	def doNext(self):
		self.source.initiateTCP(self.destination,self.dataAmount,
		self.srcPort,self.dstPort,1)
		
		self.destination.initiateTCP(self.source,0,self.dstPort,self.srcPort,0)