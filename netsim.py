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
import numpy as np
import matplotlib.pyplot as plt

print 'Setting up network objects...'
h = EventHandler()
#The following is representative of inputs
#it establishes objects - hosts routers, links, and flows
H1 = host.Host('H1',0,'TCP Reno',h)
H2 = host.Host('H2',1,'TCP Tahoe',h)
L1 = link.Link('L1',100.0,10.0,64.0,H1,H2,h)
F1 = flow.Flow('F1',H1,H2,2**22,4.0,'TCP Reno',80,80,h)
F2 = flow.Flow('F2',H2,H1,2**22,4.0,'TCP Reno',81,81,h)

print 'Simulation is beginning'

windowList = []

while(True):
	eventObject = heapq.heappop(eventQueue)		#Find the object ready to do next event
	h.setTime(eventObject[0])					#set the global time
	eventObject[1].doNext(eventObject[2])		#Do the event
	#print 'top of queue : ',eventObject[0]
	if len(eventQueue) == 0:
		break
		
	#windowList.append(H1.tcp[0].window)

print 'Simulation time: ' , h.getTime()
print 'global time var: ' , globals.time


# graph stuff

colors = "bgrcmykw"
fig1 = plt.figure(1)
fig1.suptitle('Data received by TCP receivers')
fig2 = plt.figure(2)
fig2.suptitle('Data sent by TCP senders')
fig3 = plt.figure(3)
fig3.suptitle('Window Size for the senders')

for i in range(len(flowList)):
	dataRecv = flowList[i].dstTCP.recvTime			#array of times when receiver got a packet
	dataSent = flowList[i].srcTCP.sentTime			#array of times when sender got a packet

	max_t = math.ceil(dataRecv[len(dataRecv)-1])		#maximumm time required
	recvSpeed = []										#average speed over 0.1 seconds
	sendSpeed = []
	it = 0
	count = 0
	time_axis = []
	t_step = 0

	#calculate average speed over each time slice (0.1s)
	while(t_step < max_t):
		t_step = t_step + 0.1
		while(it < len(dataRecv)):
			if dataRecv[it] < t_step:
				count=count + 1
				it = it +1
			else:
				break
		recvSpeed.append(count / 0.1)
		count = 0
	for j in range(0,len(recvSpeed)):
		time_axis.append(0.05 + .1*j)

	t_step = 0
	count = 0
	it = 0

	while(t_step < max_t):
		t_step = t_step + 0.1
		while(it < len(dataSent)):
			if dataSent[it] < t_step:
				count = count+1
				it = it +1
			else:
				break
		sendSpeed.append(count / 0.1)
		count = 0


	plt.figure(1)
	l = flowList[i].destination.name + " Port " + `flowList[i].dstPort`
	plt.plot(time_axis,recvSpeed,label=l,color=colors[i%8])

	plt.figure(2)
	l = flowList[i].source.name + " Port " + `flowList[i].srcPort`
	print l
	plt.plot(time_axis,sendSpeed,label=l,color=colors[i%8])

	k = len(flowList[i].srcTCP.windowList)
	print k
	plt.figure(3)
	plt.plot(range(1,k+1), flowList[i].srcTCP.windowList ,label=l,color=colors[i%8])

plt.figure(1)
plt.legend()
#plt.ylim(ylim)
plt.xlabel("Time (s)")
plt.ylabel("Speed (Kbps)")

plt.figure(2)
plt.legend()
#plt.ylim(ylim)
plt.xlabel("Time (s)")
plt.ylabel("Speed (Kbps)")


plt.figure(3)
plt.legend()
plt.xlabel("RTT")
plt.ylabel("Window Size")
plt.show()

print 'Simulation Completed'
