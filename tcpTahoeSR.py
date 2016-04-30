from globals import *
from eventHandler import *
from packet import IPHeader, TCPHeader, Packet
from heapq import heappush
from math import *
 
class TCPTahoeSender:
    def __init__(self, dataAmt, ipHeader, parentHost, destination, h):
        self.isSource = True
        self.ack = 0
        self.window = 1.0
        self.ssThresh = 10
        self.dupACKs = 0
        self.largestACK = 0
        self.largestSent = 1
        self.ipHeader = ipHeader
        self.parentHost = parentHost
        self.destination = destination
        self.maxSeq = dataAmt/2**10
        self.state = 'Slow start'
        self.timeoutTime = float('inf')
        self.tcpFinished = False
        self.handler = h
        self.timeoutDelay = 1.0
        self.time_list = []
       
        self.plot_list = []
   
    def doNext(self,action):
        #print 'checking timeout'
        if action == 'Check timeout' and not (self.state == 'Done'):
            t = self.handler.getTime()
            if self.timeoutTime <= t:
                self.timeout()
       
    def timeout(self):
        if self.state == 'Done':
            return
        else:
            #print 'timing out'
            self.ssThresh = self.window/2.0
            self.window = 1
            self.dupACKs = 0
            self.state = 'Slow start'
            self.largestSent = self.largestACK
            self.putPacket(self.largestACK)
       
    def recvPacket(self,p):
        self.plot_list.append(floor(self.window))
        self.time_list.append(self.handler.getTime())
        if self.state == 'Done':
            return
        elif self.state == 'Slow start':
            if p.tcpHeader.acknowledgeNumber <= self.largestACK:
                self.dupACKs += 1
                if self.dupACKs == 3:
                    self.ssThresh = self.ssThresh/2.0
                    #print self.ssThresh
                    self.window = 1
                    self.largestSent = p.tcpHeader.acknowledgeNumber
                    self.dupACKs = 0
                    self.putPacket(p.tcpHeader.acknowledgeNumber)
                    self.parentHost.beginTransmit()
                    self.state = 'Slow start'
            elif p.tcpHeader.acknowledgeNumber > self.maxSeq:
                self.state = 'Done'
                #print 'Done'
            else:
                self.largestACK = p.tcpHeader.acknowledgeNumber
                self.window = self.window + 1
                self.dupACKs = 0
                self.generatePackets()
                if self.window >= self.ssThresh:
                    self.state = 'Congestion avoidance'
                    #print 'entering Congestion avoidance'
        elif self.state == 'Congestion avoidance':
            if p.tcpHeader.acknowledgeNumber <= self.largestACK:
                self.dupACKs += 1
                if self.dupACKs == 3:
                    self.ssThresh = max(self.window,self.ssThresh)/2.0
                    self.window = 1
                    self.dupACKs = 0
                    #print self.ssThresh
                    self.largestACK = p.tcpHeader.acknowledgeNumber
                    self.putPacket(p.tcpHeader.acknowledgeNumber)
                    self.state = 'Slow start'
                    #print 'entering slow start'
            elif p.tcpHeader.acknowledgeNumber > self.maxSeq:
                self.state = 'Done'
                #print 'Done'
            else:
                self.largestACK = p.tcpHeader.acknowledgeNumber
                self.window = self.window+(1.0/int(self.window))
                self.dupACKs = 0
                self.generatePackets()
               
    def putPacket(self,seq):
 
        #print 'putting packet',seq
        tcpHeader = TCPHeader(seq,self.ack,self.window)
        ipHeader = self.ipHeader
        p = Packet(tcpHeader,self.ipHeader,1024,self.parentHost,self.parentHost)
        self.parentHost.queue.append(p)
        self.largestPacketSent = seq
               
    def generatePackets(self):
        #print 'generating packets'
        for i in range(1+int(self.largestPacketSent),int(self.largestACK + self.window)):
            if i > self.maxSeq:
                return
            self.putPacket(i)
        heappush(eventQueue, (self.timeoutTime, self, 'checkTimeout') )
        self.parentHost.beginTransmit()
        #print 'largest ACK is',self.largestACK
           
class TCPTahoeReceiver:
    def __init__(self, size, ipHeader, parentHost, destination):
        self.isSource = False
        self.seq = 0
        self.ack = 0
        self.windowStart = 1
        self.windowList = []
        for i in range(2**14):
            self.windowList.append(0)
        self.ipHeader = ipHeader
        self.lasSeqReceived = 0
        self.parentHost = parentHost
        self.recvTime = []
        self.recvPacketCount = 0
        self.destination = destination
       
    def recvPacket(self,p):
        i = p.tcpHeader.sequenceNumber - self.windowStart
        self.windowList[i] = 1
        need = 0
        for i in range(len(self.windowList)):
            if not self.windowList[i]:
                need = i
                break
        if need:
            ack = need + self.windowStart
            tcpHeader = TCPHeader(ack,ack,len(self.windowList))
            p = Packet(tcpHeader,self.ipHeader,64,self.parentHost,self.parentHost)
            self.parentHost.queue.append(p)
            self.parentHost.beginTransmit()