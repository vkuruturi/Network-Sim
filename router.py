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
	def _init_(self, name, ipAddress, h):
		self.name = name;
		self.ipAddress = ipAddress
		self.links = []
		self.queue = []
		routerList.append(self)
		self.handler = h;
		self.distancetables = defaultdict(dict);
		self.neighbors = [];
		distancetables[self][self] = [0, self];
		for link in links:
			if link.c1 == self:
				self.neighbors.append([link.c2, link]);
				distancetables[self][link.c2] = [link.cost, link.c2];
			else:
				self.neighbors.append([link.c1, link]);
				distancetables[self][link.c1] = [link.cost, link.c1];
		self.sendDSDV();
	def sendDSDV(self):
		DSDV_packet = RouterPacket(64, true, distancetables[self], self)
		for link in links:
			heappush(eventQueue, (self, self.h.getTime() + DSDV_packet.size/(link.rate), "SEND DSDV"))
			heappush(eventQueue, (self, self.h.getTime() + 1, "NEW DSDV"))
			link.recvPacket(DSDV_packet);
	def recvPacket(self, p):
		if p.isDistancePacket:
			self.distancetables[p.sender] = p.DSDV_data
			for key in self.distancetables[self]:
				min_cost = self.distancetables[self][key][0];
				min_rout = key;
				for key2 in self.distancetables[self]:
					cost = self.distancetables[self][key2][0] + self.distancetables[key2][key][0];
					if (cost < min_cost):
						min_cost = cost;
						min_rout = key2;
				distancetables[self][key][1] = min_rout;

		else:
			p.immSender = self;	
			self.sendPacket(p);
	def sendPacket(self, p):
		min_ipdiff = 10000000000000000;
		min_key;
		for key in self.distancetables:
			if ((key.ipAddress - p.ipHeader.destinationAddress) < min_ipdiff):
				min_key = key
		send_to = distancetables[self][min_key][1];
		time = self.handler.getTime();

		for neighbor in neighbors:
			if (neighbor[0] == send_to):
				neighbor[1].recvPacket(p);
				heappush(eventQueue, ((time+(p.size / neighbor[1].rate)), self, "send_packet"))
				break

	def doNext(self, action):
		if action == "NEW DSDV":
			self.sendDSDV();