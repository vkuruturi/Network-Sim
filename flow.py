from globals import *
from heapq import heappush

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
		heappush(eventQueue,(self.startTime,self,'init'))
		
	def doNext(self,action):
		if action == 'init':
			self.source.initiateTCP(self.destination,self.dataAmount,1)
			
			self.destination.initiateTCP(self.source,0,0)
