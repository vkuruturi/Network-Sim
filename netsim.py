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
H1 = host.Host('H1',0,'TCP Tahoe',h)
H2 = host.Host('H2',1,'TCP Tahoe',h)
H3 = host.Host('H3', 2, 'TCP Tahoe', h)
H4 = host.Host('H4', 3, 'TCP Tahoe', h)
R1 = router.Router('R1', 4, h)
R2 = router.Router('R2', 5, h)
R3 = router.Router('R3', 6, h)
L1 = link.Link('L1',10.0,10.0,64.0,H1,R1,h)
L2 = link.Link('L2', 10.0, 10.0, 64.0, R1, R2, h)
L3 = link.Link('L3', 10.0, 10.0, 64.0, R2, H2, h)
L4 = link.Link('L4', 10.0, 10.0, 64.0, H3, R1, h)
L5 = link.Link('L5', 10.0, 10.0, 64.0, H4, R3, h)
L6 = link.Link('L6', 10.0, 10.0, 64.0, H2, R2, h)
F1 = flow.Flow('F1',H1,H2,2**17,4.0,'TCP Tahoe',80,80,h)
F2 = flow.Flow('F2',H2,H1,2**15,4.0,'TCP Tahoe',81,81,h)
F3 = flow.Flow('F3', H3, H1, 2**15, 4.0, 'TCP Tahoe', 82, 82, h);
F4 = flow.Flow('F4', H4, H3, 2**15, 4.0, 'TCP Tahoe', 83, 83, h);

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