class Router:
	address = 0
	table = [[1, 2], [0, 2], [0, 1], [0, 1, 2]]
	def __init__(self, address):
		self.address = address
	def route(self, source, destination, packet):
		return Event(source, destination, packet)
	input_buffer = []

class Event:
	def __init__(self, source, destination, packet):
		self.source = source
		self.destination = destination
		self.packet = packet
class EventHandler:
	# Input routers and links
	def routers(self):
		self.routers = raw_input("Please enter routers: ").split(str = " ")
	def links(self):
		self.links = raw_input("Please enter links: ").split(str = " ")
	def hosts(self):
		self.hosts = raw_input("Please enter hosts: ").split(str = " ")
	def route(self, packet):
		pass

class Link:
	def __init__(self,link_id, link_rate, link_delay, link_buffer_size, con1, con2):
		self.id = link_id						#Name string
		self.rate = link_rate					#Rate in Mbps
		self.delay = link_delay					#link delay in ms
		self.buffer_size = link_buffer_size 	#Buffer size in KB
		(con1.con).append(con2)
		(con2.con).append(con1)


class Host:
	def __init__(self,name,ip_address):
		self.con = []
		self.name = name
		self.ip = ip_address
		
class Flow:
	def __init__(self,flow_id, flow_source, flow_destination, flow_data_amt, flow_start_time, algorithm):
		self.id = flow_id 					#Name string
		self.src = flow_source				#Actual host object
		self.dst = flow_destination			#Actual host object
		self.amt = flow_data_amt			#Data amount in Mebibytes (I think)
		self.start_time = flow_start_time	#Start time in seconds

		number_of_packets = int(self.amt*2**10)	#each packet is assumed fixed at 1024 bytes

		for i in range(number_of_packets):
			j = 0
			p = Packet(0 , 0 , self.src, self.dst , ' ' , i , j , 1 , 0.5, ' ',self.src)


class Packet:
	def __init__(self,tcp_source_port,tcp_destination_port,ip_source_address,
		ip_dest_address,ip_protocol,tcp_sequence_number,tcp_acknowledge_number,
		tcp_window,ip_time_to_live, tcp_flags,phy_location):
		pass

H1 = Host('H1' , 0)
H2 = Host('H2' , 1)
L1 = Link('L1', 10.0 , 10.0 , 64.0, H1, H2)
F1 = Flow('F1' , H1 , H2 , 20.0 , 1.0, 'tcp_reno')

host_list = []
host_list.append(H1)
host_list.append(H2)

link_list = []
link_list.append(L1)

flow_list = []
flow_list.append(F1)
