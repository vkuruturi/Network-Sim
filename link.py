from globals import *
from eventHandler import *
from heapq import heappush

class Link:
    def __init__(self, name, rate, delay, buffer, connection1, connection2, h):
        self.name = name                     #string representation
        self.rate = rate * 1e6 / 8.0         #convert from Mbps to Bps
        self.delay = delay/1000.0            #convert from ms to s
        self.bufferSize = buffer * 1000.0    #convert from KB to B
        self.c1 = connection1                #pointer to one of the hosts
        self.c2 = connection2     
        self.handler = h                     #h has the global time
        
        self.c1_ltd = 0.0                    #at each this time the link will have...
        self.c2_ltd = 0.0                    #no packets from that connection...
                                             #ltd = last time to delivery
        self.c1.setLink(self)                 #add this link information to...
        self.c2.setLink(self)                  #each object it connects
        
        self.bufferBytes = 0                 #amount of bytes in link buffer
        self.queue = []                      #packet objects in link's queue/buffer
        
        self.bufferList = []
        self.bufferTimestamps = []

        self.droppedPackets = []
        self.droppedPacketsTimestamps = []

    def recvPacket(self,p):
        t = self.handler.getTime()                      	#store current time in t
        print 'current size is',self.bufferBytes
        #self.bufferList.append(self.bufferBytes)

        if self.bufferBytes + p.size <= self.bufferSize:	#if buffer full, reject packet
            if p.immSender == self.c1:                      #wait until link is clear of
                ttd = max(t,self.c2_ltd) + self.delay        #the other hosts's packets.
            elif p.immSender == self.c2:
                ttd = max(t,self.c1_ltd) + self.delay
            else:
                print 'Error, neither sender',self.c1.name,'nor',self.c2.name,'may send to link',self.name
            self.queue.append(p)
            self.bufferBytes += p.size
            self.bufferList.append(self.bufferBytes)
            self.bufferTimestamps.append(globals.time)
            heappush(eventQueue, (ttd,self,'send') )		#schedule an event where the packet is tranfered

        else:
            self.droppedPackets.append(1)
            self.droppedPacketsTimestamps.append(globals.time)
            print p.immSender.name,'dropped a packet on link',self.name
            
    def sendPacket(self,p):
        self.bufferBytes -= p.size
        self.bufferList.append(self.bufferBytes)
        self.bufferTimestamps.append(globals.time)

        if p.immSender == self.c1:
            self.c2.recvPacket(p)
        elif p.immSender == self.c2:
            self.c1.recvPacket(p)
        else:
            print 'Error packet does not match either object'
        
    def doNext(self,action):
        if action == 'send':
            p = self.queue.pop(0)
            if p.immSender == self.c1:
                dest = self.c2
            else:
                dest = self.c1
            print 'Link',self.name,'is sending packet',p.tcpHeader.sequenceNumber,'from',p.immSender.name,'to',dest.name
            self.sendPacket(p)

        
            
        