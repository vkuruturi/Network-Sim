#The following classes define all the contents of a packet

import packet


#This line marks the start of TCP algorithm definitions

class TCPReno:
	

class Link:
	def __init__(self,name,rate,delay,buffer,c1,c2):
		self.name = name
		self.rate = rate
		self.delay = delay
		self.bufferSize = buffer
		self.connection1 = c1
		self.connection2 = c2
		
		self.connection1.connection.append(self.connection2)
		self.connection2.connection.append(self.connection1)
		self.transmitting = 0
		self.queue = []
		
		linkList.append(self)
		
	def receive(p):
		if len(self.queue) < bufferSize:
			queue.append(p)

class Host:
	def __init__(self,name,ipAddress):
		self.name = name
		self.ipAddress = ipAddress
		
		self.connection = [] #Note, this should only ever be 1
							 #It is only a list for consistency with routers
							 
		hostList.append(self)
		
		#Remember to include maximum packet sequence somewhere
		
	def putPacket(ipHeader,tcpHeader):
		p = Packet(ipHeader,tcpHeader,self)	#create packet
		link.receive(p)						#send packet to link
		
class Flow:
	def __init__(self,name,source,destination,amount,start):
		self.name = name
		self.source = source
		self.destination = destination
		self.dataAmount = amount
		self.startTime = start
		
		flowList.append(self)
		
def eventSearch():
	for i in range(hostList):
		tempList = getEvents
		for j in 
	for i in range(linkList):
	for i in range(flowList):
def advanceTimeStep():
	pass
	
#Global Necessities start
time = 0
eventQueue = []
#The event queue contains a list of tuples:
#The object performing the event along with the time it is performed

#Global Necessities end

hostList = []
linkList = []
flowList = []
	
H1 = Host('H1',0)
H2 = Host('H2',1)
L1 = Link('L1',10,10,1000,H1,H2)



advanceTimeStep()
