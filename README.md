# Network-Sim

##Instructions on how to set up the network:

The network topology is generated by parsing the input.txt file.  The format is as follows:

Hosts:
1. String name of host
2. IP Address, decimal
3. Algorithm running on host as source
Example:
Host1,1,TCP Reno
Host2,3,TCP Tahoe

Routers:
1. String name of router
2. IP Address, decimal
Example:
Router1,2

Links:
1. String name of link
2. rate in Mbps
3. delay in ms
4. buffer size in KB
5. Name of first connection
6. Name of second connection
Example:
Link1,10,1,64,Host1,Router1

Flows:
1. String name of flow
2. string name of source host
3. string name of destination host
4. exponent of 2 (i.e. 22 -> 2^22) bytes in flow
5. Start time of flow in seconds
6. port number of receiver
7. port number of destination
Example:
Flow1,Host1,Host2,12,1,80,80
