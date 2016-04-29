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

section = [0,0,0,0]

print 'Setting up network objects...'
h = EventHandler()
###The following is representative of inputs
#it establishes objects - hosts routers, links, and flows
# H1 = host.Host('H1',0,'TCP Reno',h)
# H2 = host.Host('H2',1,'TCP Tahoe',h)
# L1 = link.Link('L1',10.0,10.0,64.0,H1,H2,h)
# F1 = flow.Flow('F1',H1,H2,2**22,4.0,'TCP Reno',80,80,h)
# F2 = flow.Flow('F2',H2,H1,2**22,4.0,'TCP Reno',81,81,h)


with open('input.txt') as input:
	lines = input.readlines
	for line in input:
		line = line.rstrip()
		print section

		if line == 'Hosts:':
			section[0] = 1
			continue
#		elif line == 'Routers:':
#			section[1] = 1
#			section[0] = 0
#			continue
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
			print 'HI'

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

colors = "bgrcmykw"
fig1 = plt.figure(1)
fig1.suptitle('Data received by TCP receivers')
fig2 = plt.figure(2)
fig2.suptitle('Data sent by TCP senders')
fig3 = plt.figure(3)
fig3.suptitle('Window Size for the senders')

#plot sender/receiver rate, sender window size
for i in range(len(flowList)):
	dataRecv = flowList[i].dstTCP.recvTime			#array of times when receiver got a packet
	dataSent = flowList[i].srcTCP.sentTime			#array of times when sender got a packet

	max_t = math.ceil(max(dataRecv))		#maximumm time required
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

#plot link statistics
print len(linkList)
for i in range(len(linkList)):
	print i
	bufferSz = linkList[i].bufferList
	times = linkList[i].bufferTimestamps
	droppedPackets = linkList[i].droppedPackets
	times2 = linkList[i].droppedPacketsTimestamps
	plt.figure(4)
	l = linkList[i].name
	#print len(bufferSz)#, '   ',len(times)
	plt.plot(times,bufferSz,label=l,color=colors[i%8])
	plt.figure(5)
	plt.plot(times2,droppedPackets,label=l,color=colors[i%8])

plt.figure(4)
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Buffer size (bytes)")

plt.figure(5)
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Dropped Packet Count")

for i in range(len(hostList)):
	dataSent = hostList[i].dataSent
	dataRecv = hostList[i].dataReceived

	dataSentTimestamps = hostList[i].dataSentTimestamps
	dataRecvTimestamps = hostList[i].dataReceivedTimestamps

	max_t = max(max(dataSentTimestamps),max(dataRecvTimestamps))

	recvSpeed = []
	sendSpeed = []

	it = 0
	count = 0
	time_axis_recv = []
	time_axis_send = []
	t_step = 0

	while(t_step < max_t):
		t_step = t_step +0.1
		while (it < len(dataRecv)):
			if dataRecvTimestamps[it] < t_step:
				count=count + dataRecv[it]
				it = it +1
			else:
				break
		recvSpeed.append((count / 1024) / 0.1)
		count = 0

	for j in range(0,len(recvSpeed)):
		time_axis_recv.append(0.05 + .1*j)

	t_step = 0
	count = 0
	it = 0

	while(t_step < max_t):
		t_step = t_step +0.1
		while(it<len(dataSent)):
			if dataSentTimestamps[it] < t_step:
				count = count + dataSent[i]
				it = it +1
			else:
				break
		sendSpeed.append((count /1024) / 0.1)
		count = 0

	for j in range(0, len(sendSpeed)):
		time_axis_send.append(0.05 + .1*j)


	plt.figure(6)
	l = hostList[i].name + ' Receive'
	plt.plot(time_axis_recv,recvSpeed,label=l,color=colors[i%8])

	plt.figure(7)
	l = hostList[i].name + ' Send'
	plt.plot(time_axis_send, sendSpeed,label=l,color=colors[i%8])

plt.figure(6)
plt.legend()
plt.suptitle("Host receive rate")
plt.ylabel("Rate (Kbps)")
plt.xlabel("Time (s)")

plt.figure(7)
plt.legend()
plt.suptitle("Host send rate")
plt.ylabel("Rate (Kbps)")
plt.xlabel("Time (s)")


plt.show()



print 'Simulation Completed'

