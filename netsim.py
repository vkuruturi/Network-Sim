from globals import *
from eventHandler import *
import heapq
import host
import link
import packet
import flow
import tcpRenoSR

import numpy as np
import matplotlib.pyplot as plt
import math
	
h = EventHandler()

H1 = host.Host('H1',0,'TCP Reno',h)
H2 = host.Host('H2',1,'TCP Reno',h)
L1 = link.Link('L1',10.0,10.0,64.0,H1,H2,h)
F1 = flow.Flow('F1',H1,H2,2**22,1.0,'TCP Reno',80,80,h)

print hostList[0]

while(True):
	eventObject = heapq.heappop(eventQueue)	#Find the object ready to do next event
	h.setTime(eventObject[0])
	eventObject[1].doNext()					#Do the event
	print 'top of queue : ',eventObject[0]

			#advance the time to the input value
									#Still needs to be implemented ^
	if len(eventQueue) == 0:
		break

print 'Simulation time: ' , h.getTime()
print 'global time var: ' , globals.time
# graph stuff		
for i in range(len(flowList)):
	data = flowList[i].destination.tcp.recvTime
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

	fig = plt.figure()
	plot1 = fig.add_subplot(111)
	print 'size of time_axis: ', len(time_axis)
	print 'size of speed    : ', len(speed)
	plot1.plot(time_axis,speed,color='blue')
	plot1.set_xlim([0,max_t])
	plot1.set_ylim([0,max(speed)])
	plt.show()	
		
		
print 'Simulation Completed'
