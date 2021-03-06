
from globals import *
from heapq import heappush

class Flow:
	def __init__(self,name,source,destination,amount,start,srcPort,dstPort,h):
		self.name = name
		self.source = source
		self.destination = destination
		self.dataAmount = amount
		self.startTime = start
	#	self.Algorithm = algo
		self.srcPort = srcPort
		self.dstPort = dstPort
		self.srcTCP = []
		self.dstTCP = []
		#flowList.append(self)
		heappush(eventQueue,(self.startTime,self,'init'))
		
	def doNext(self,action):
		#create TCP objects at the hosts
		if action == 'init':
			self.source.initiateTCP(self.destination,self.dataAmount,1,self)
			
			self.destination.initiateTCP(self.source,0,0,self)