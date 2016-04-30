from globals import *
from eventHandler import *
from collections import defaultdict
import heapq
from heapq import heappush
import host
import link
import packet
import flow
import tcpRenoSR

class Router:
	def __init__(self, name, ipAddress, h):
		self.name = name;
		self.ipAddress = ipAddress
		self.links = []
		self.queue = []
		routerList.append(self)
		self.handler = h;
		self.distancetables = defaultdict(dict); #Distance Vector table, each entry is
		#a tuple of the minimum route (i.e. which host or router to send it to) and the
		#minimum cost to send to
		self.neighbors = [];
		self.distancetables[self][self] = [0, self];
		self.initialized = 0;
		self.isRouter = 1;
		self.count = 0;
	def setLink(self, link):
		self.links.append(link);
		#print "appended ", link.name;
	def sendDSDV(self):
		#print self.handler.getTime(), "Sending DSDV"
		# if (self.initialized == 0):
		# 	self.initialized = 1;
		stop = 0;
		for host in self.handler.getHostList():
			for tcpConnection in host.tcp:
				if (tcpConnection.isSource == 1):
					stop = tcpConnection.tcpFinished;
		if (stop == 1):
			return
		#print self.name, "is sending its DSDV data"
		self.updateDSDV();
		# for link in self.links:
		# 	print link.name
		DSDV_packet = packet.RouterPacket(64, self.distancetables[self], self)
		DSDV_packet.immSender = self;
		for link in self.links:
			link.recvPacket(DSDV_packet);
			heappush(eventQueue, (self.handler.getTime() + DSDV_packet.size/(link.rate), self, "SEND DSDV"))
			#heappush(eventQueue, (self.handler.getTime() + 1, self, "NEW DSDV"))
	def recvPacket(self, p):
		self.updateDSDV();
		if p.isDistancePacket:
			self.distancetables[p.sender] = p.DSDV_data
			for key in p.DSDV_data:
				if not key in self.distancetables[self]:
					self.distancetables[self][key] = [10000000000000000, key];
			for key in self.distancetables[self]:
				if not key in self.distancetables:
					for key2 in self.distancetables[self]:
						self.distancetables[key][key2] = [100000000000000, key2];
				else:
					for key2 in self.distancetables[self]:
						if not key2 in self.distancetables[key]:
							self.distancetables[key][key2] = [100000000000000, key2];
				self.distancetables[key][key] = [0, key];
			#print self.name, 'received distance packet before updating is: ', self.distancetables
			for key in self.distancetables[self]:
				min_cost = self.distancetables[self][key][0];
				min_rout = key;
				for key2 in self.distancetables[self]:
					if key2.isRouter == 1:
						#print key, key2
						cost = self.distancetables[self][key2][0] + self.distancetables[key2][key][0];
						if (cost < min_cost):
							min_cost = cost;
							min_rout = key2;
				self.distancetables[self][key][1] = min_rout;

		elif (not(p.isDistancePacket)):
			#print "NOT DISTANCE"
			p.immSender = self;	
			self.count = self.count + 1;
			if  (self.count % 500) == 0:
				self.sendDSDV()
			self.sendPacket(p);
	def sendPacket(self, p):
		min_ipdiff = 10000000000000000;
		min_key = self;
		for key in self.distancetables[self]:
			#print 'key name', key.name
			#print 'key ip address', key.ipAddress, 'packet ipAddress', p.ipHeader.destinationAddress;
			difference = key.ipAddress - p.ipHeader.destinationAddress;
			if (difference < 0) :
				difference = difference * (-1);
			if (difference < min_ipdiff):
				min_ipdiff = difference
				min_key = key
		send_to = self.distancetables[self][min_key][1];
		time = self.handler.getTime();
		#print self.name, 'is sending packet ', p.tcpHeader.sequenceNumber, 'with source', p.origSender.name, 'to ', send_to.name,

		for neighbor in self.neighbors:
			if neighbor[0].isRouter == 0:
				if neighbor[0].ipAddress == p.ipHeader.destinationAddress:
					neighbor[1].recvPacket(p);
					heappush(eventQueue, ((time+(p.size / neighbor[1].rate)), self, "send_packet"))
					return

		for neighbor in self.neighbors:
			if neighbor[0].isRouter == 1:
				if (neighbor[0] == send_to):
					neighbor[1].recvPacket(p);
					heappush(eventQueue, ((time+(p.size / neighbor[1].rate)), self, "send_packet"))
					return

	def updateDSDV(self):
		#print self.name, "is updating its DSDV"
		for link in self.links:
			#print 'link name: ', link.name
			if link.c1 == self:
				#print 'other side of link', link.c2.name
				self.neighbors.append([link.c2, link]);
				if link.c2.isRouter == 1:
					self.distancetables[self][link.c2] = [link.getAndUpdateCost(), link.c2]
			else:
				#print 'other side of link', link.c1.name
				self.neighbors.append([link.c1, link]);
				if link.c1.isRouter == 1:
					self.distancetables[self][link.c1] = [link.getAndUpdateCost(), link.c1]
		#print 'new distancetables:', self.distancetables
	def doNext(self, action):
		return