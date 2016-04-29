print 'Importing modules...'

from globals import *
from eventHandler import *
import heapq
import host
import link
import packet
import flow
import tcpRenoSR
import math
import router
import numpy as np
import matplotlib.pyplot as plt
	
print 'Setting up network objects...'
h = EventHandler()
#The following is representative of inputs
#it establishes objects - hosts routers, links, and flows

#section represents which section of input the code is in
section = [0,0,0,0]
#Host, Routers, Links, Flows

hostList = []
routerList = []
linkList = []
flowList = []
inputList = []

with open('input.txt') as input:
	lines = input.readlines
	for line in input:
		line = line.rstrip()
		print section
		if line == 'Hosts:':
			section[0] = 1
			continue
		elif line == 'Routers:':
			section[1] = 1
			section[0] = 0
			continue
		elif line == 'Links:':
			section[2] = 1
			section[1] = 0
			section[0] = 0
			continue
		elif line == 'Flows:':
			section[3] = 1
			section[2] = 0
			section[1] = 0
			section[0] = 0
			continue
			
		inputList = line.split(',')
		if section[0]:
			name = inputList[0]
			ip = int(inputList[1])
			algo = inputList[2]
			H = host.Host(name,ip,algo,h)
			hostList.append(H)
			
		if section[1]:
			name = inputList[0]
			ip = int(inputList[1])
			R = router.Router(name,ip,h)
			routerList.append(R)
			
		if section[2]:
			name = inputList[0]
			rate = float(inputList[1])
			delay = float(inputList[2])
			buffer = float(inputList[3])
			c1 = inputList[4]
			c2 = inputList[5]
			for i in range(len(hostList)):
				if hostList[i].name == c1:
					C1 = hostList[i]
			for i in range(len(routerList)):
				if routerList[i].name == c1:
					C1 = routerList[i]
					
			for i in range(len(hostList)):
				if hostList[i].name == c2:
					C2 = hostList[i]
			for i in range(len(routerList)):
				if routerList[i].name == c2:
					C2 = routerList[i]
					
			L = link.Link(name,rate,delay,buffer,C1,C2,h)
			linkList.append(L)
			
		if section[3]:
			print 's3'
			name = inputList[0]
			c1 = inputList[1]
			c2 = inputList[2]
			for i in range(len(hostList)):
				if hostList[i].name == c1:
					C1 = hostList[i]
			for i in range(len(routerList)):
				if routerList[i].name == c1:
					C1 = routerList[i]
					
			for i in range(len(hostList)):
				if hostList[i].name == c2:
					C2 = hostList[i]
			for i in range(len(routerList)):
				if routerList[i].name == c2:
					C2 = routerList[i]
			dataAmt = 2**int(inputList[3])
			startTime = float(inputList[4])
			p1 = int(inputList[5])
			p2 = int(inputList[6])
			F = flow.Flow(name,C1,C2,dataAmt,startTime,p1,p2,h)
			flowList.append(F)
	
'''
H1 = host.Host('H1',0,'TCP Reno',h)
H2 = host.Host('H2',2,'TCP Reno',h)
R1 = router.Router('R1', 1, h)
L1 = link.Link('L1',10.0,10.0,64.0,H1,R1,h)
L2 = link.Link('L2', 10.0, 10.0, 64.0, H2, R1, h)
F1 = flow.Flow('F1',H1,H2,2**22,4.0,80,80,h)
F2 = flow.Flow('F2',H2,H1,2**22,4.0,81,81,h)
'''
print 'Simulation is beginning'

windowList = []

while(True):
	eventObject = heapq.heappop(eventQueue)		#Find the object ready to do next event
	h.setTime(eventObject[0])
	#print eventObject[2].name					#set the global time
	eventObject[1].doNext(eventObject[2])		#Do the event
	#print 'top of queue : ',eventObject[0]
	if len(eventQueue) == 0:
		break
		
	#windowList.append(H1.tcp[0].window)

print 'Simulation time: ' , h.getTime()
print 'global time var: ' , globals.time
# graph stuff	

'''	
for i in range(len(flowList)):
	data = flowList[i].destination.tcp[0].recvTime
	print 'First packet received at : ', data[0]
	print 'Size of recvTime         : ', len(data)
	max_t = math.ceil(data[len(data)-1])
	print 'max_t                    : ', max_t
	speed = []
	it = 0
	count = 0
	time_axis = []
	t_step = 0
	while(t_step < max_t):
		t_step = t_step + 0.1
		while(it < len(data)):
			if data[it] < t_step:
				count=count + 1
				it = it +1
			else:
				break
		print 'count: ',count
		speed.append(count *1024 / 0.1)
		count = 0
	for j in range(0,len(speed)):
		time_axis.append(0.05 + .1*j)

	plt.plot(H1.tcp[0].windowList)
'''
plt.plot(L1.bufferList)
'''
	fig = plt.figure()
	plot1 = fig.add_subplot(111)
	print 'size of time_axis: ', len(time_axis)
	print 'size of speed    : ', len(speed)
	plot1.plot(time_axis,speed,color='blue')
	plot1.set_xlim([0,max_t])
	plot1.set_ylim([0,max(speed)])
'''
plt.show()	

		
print 'Simulation Completed'