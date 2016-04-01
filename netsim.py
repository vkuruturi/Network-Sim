from globals import *
from eventHandler import *
import heapq
import host
import link
import packet
import flow
import tcpReno
	
h = EventHandler()

H1 = host.Host('H1',0,'TCP Reno',h)
H2 = host.Host('H2',1,'TCP Reno',h)
L1 = link.Link('L1',10.0,10.0,64.0,H1,H2,h)
F1 = flow.Flow('F1',H1,H2,2**20,1.0,'TCP Reno',80,80,h)



while(True):
	eventObject = heapq.heappop(eventQueue)	#Find the object ready to do next event
	h.setTime(eventObject[0])
	eventObject[1].doNext()					#Do the event
	print eventObject[0]

			#advance the time to the input value
									#Still needs to be implemented ^
	if len(eventQueue) == 0:
		break
		
print 'Simulation Completed'