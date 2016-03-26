class Packet:
	def __init__(TCPHeader,IPHeader,immediateSender):
		self.tcpHeader = TCPHeader
		self.ipHeader = IPHeader
		self.immediateSender = immediateSender



    class TCPHeader:
	    def __init__(srcPort,dstPort,seq,ack,cwnd):
            self.sourcePort = srcPort
            self.destinationPort = dstPort
            self.sequenceNumber = seq
            self.acknowledgeNumber = ack
            self.windowSize = cwnd

        #The above are important to the simulation
        #The following were left out because they are likely irrelevent
        #Data offset, Reserved, flags, urgent pointer, checksum, options,
        #padding, Data

    class IPHeader:
	    def __init__(self,timeToLive,sourceAddress,destinationAddress):
            self.timeToLive = timeToLive
            self.sourceAddress = sourceAddress
            self.destinationAddress = destinationAddress
        #The above are important to the simulation
        #The following were left out because they are likely irrelevant
        #Version, header length, TOS, total length, identification, flags,
        #header checksum, fragment offset, protocol, options

#This line marks the end of the packet class definitions