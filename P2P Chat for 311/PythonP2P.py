import socket
import threading
import sys
from random import randrange, seed
from time import sleep

#############################
#######PYTHON P2P CHAT#######
#############################
'''
Basic Rundown of internal commands
%C_ is a generic connect command, sent to the mediator before getting a list of peers
%P_ is an "Add Peer" command, which is processed by the client as "Add whatever's after this to the list of peers"
%A_ is the alive check/alive response. The mediator sends these, then the clients send them back.
%D_ is the "Remove Peer" command, sent my the mediator when a peer does not respond to %A_
%S_ is the command to get a valid unoccupied port
'''
def rePrompt():
    #sys.stdout.write(name + ": ")
	sys.stdout.write("<" + name + ">")
	sys.stdout.flush()

def listenOnSocket(L, returned):
	while 1:
		try:
			raw = L.recvfrom(1024)
		except:
			continue #If the listen is interrupted by a send, restart it
		#print("Data Received")
		data = raw[0].decode('utf-8')
		address = raw[1]
		if data[:1] != "%":
			returned.append("MSG&"+str(data))
		else:
			if data[:3] == "%C_" or data[:3] == "%S_":
				data = data + address[0] + ":" + str(address[1])
			returned.append(str(data))

#Functions for processing input from socket
def processCommand(command, peers, socket):
	if command[:3] == "%P_":
		print("got Peer data")
		addPeer(command[3:], peers)
	elif command[:3] == "%D_":
		removePeer(command[3:], peers)
	elif command[:3] == "%A_":
		confirmAlive(command[3:], socket)
	elif command[:3] == "%S_":
		connectPeer(socket, command[3:])
	elif command[:3] == "%C_":
		sharePeer(command[3:], peers, socket)
	else:
		print("Unknown Command: " + command)
def addPeer(data, peers):
	ip, port = data.split(":")
	newTuple = (ip, int(port))
	peers.append(newTuple)
	print("Peer Added")
	print(peers)
def removePeer(data, peers):
	print(data + "--->REMOVEPEER")
	ip, port = data.split(":")
	newTuple = (ip, int(port))
	peers.remove(newTuple)
def confirmAlive(data, socket):
	print(data)
	ip, port = data.split(":")
	if ip == "0.0.0.0":
		ip = "localhost"
	newTuple = (ip, int(port))
	socket.sendto(("%A_" + ownAddr[1][0] + ":" + str(ownAddr[1][1])).encode('utf-8'), newTuple)
def printToConsole(data):
	#Assume 80 character max width
	print("\r" + "                                                                               " + "\r" + data)
	rePrompt()
def connectPeer(socket, command):
	ip, port = command.split(':')
	port = int(port)
	address = (ip, port)
	taken = True
	while taken:
		taken = False #port is not taken
		newPort = randrange(55556, 56555) #get a new port
		for each in peers:
			if newPort==each[1]: #If the port matches a peer port
				taken = True #obviously it's taken
	#When you get a free port, send %R_<port> to client
	print(ip)
	socket.sendto((str(newPort)).encode('utf-8'), address)
def sharePeer(address, peers, socket):
	connectorString = "%P_" + ownAddr[1][0] + ":" + str(ownAddr[1][1]) + "$"
	swarmString = "%P_" + address
	for peer in peers:
		if (peer == ownAddr[1]):
			print("Skipping own address")
			continue
		connectorString = connectorString + peer[0] + ":" + str(peer[1]) + "$"
		socket.sendto(swarmString.encode('utf-8'), (peer[0], peer[1]))
	ip, port = address.split(':')
	port = int(port)
	newPeer = (ip, port)
	socket.sendto(connectorString.encode('utf-8'), newPeer)
	peers.append(newPeer)
def checkAlive(peers, socket):
	checkAliveString = "%A_" + ownAddr[1][0] + ":" + str(ownAddr[1][1])
	for peer in peers:
		if (peer == ownAddr[1]):
			print("Skipping own address")
			continue
		socket.sendto(checkAliveString.encode('utf-8'), (peer[0], peer[1]))
		peers.remove(peer)
#Functions for sending things
def sendMessage(S, peers, name):
	while 1:
		message = input("<" + name + ">")
		message = "<" + name + ">" + message
		for peer in peers:
			S.sendto(message.encode('utf-8'), (peer))
def medListen(L, b):
	while 1:
		try:
			raw = L.recvfrom(1024)
		except:
			print("socket overload")
			continue
		if ((raw[0]).decode('utf-8'))[:3] == "%C_":
			rawTuple = raw[1]#(raw[0].decode[3:], raw[1])
			self.medConnect(rawTuple)
		elif ((raw[0]).decode('utf-8'))[:3] == "%S_":
			taken = True
			while taken:
				taken = False #port is not taken
				newPort = randrange(55556, 56555) #get a new port
				for each in self.currentSwarm:
					if newPort==each[1]: #If the port matches a peer port
						taken = True #obviously it's taken
			#When you get a free port, send %R_<port> to client
			print(raw[1][0])
			self.medSocketS.sendto((str(newPort)).encode('utf-8'), (raw[1][0], raw[1][1]))
		else:
			print("Error: Invalid Command: " + (raw[0]).decode('utf-8'))
###############################################
####################END DEFS###################
###############################################
# try:
	# Mediator(55554, "localhost", 55555)
# except:
	# print("Mediator Already Active")
peers = [] #tuples of all peer addresses
commandQueue = [] #stores actions to be processed in main thread
mode = int(input("Enter mode(1=connect, 2=host): "))
if mode == 1:
	#Temp Socket
	Tl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#registered Socket
	Tr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	name = str(input("Enter Username:"))
	ip = str(input("Enter IP of Peer/Linker:"))
	peerPort = int(input("Enter Port of Peer/Linker:"))
	#necessary to receive from mediator
	port = 12345
	#bind socket for listening
	Tl.bind(('localhost', port))

	#Very Temporary code
	#Send a request for new port
	Tl.sendto(("%S_").encode('utf-8'), (ip, peerPort))
	raw = Tl.recvfrom(1024)
	port = int(raw[0].decode('utf-8'))
	#Print some debug info (message ip:port)
	print (raw[0].decode('utf-8') + " " + raw[1][0] + ":" + str(raw[1][1]))
	Tr.bind(('', port))
	Tr.sendto(("test").encode('utf-8'), ("localhost", 12345))
	ownAddr = Tl.recvfrom(1024)
	print(ownAddr[0].decode('utf-8'))
	Tl.close()
	#bind Tr to approved port
	#Tr.bind(('', port))
	#request list of peers
	Tr.sendto(("%C_").encode('utf-8'), (ip, peerPort))
	raw = Tr.recvfrom(1024)
	try:
		print(raw[0].decode('utf-8'))
		tempArray = raw[0].decode('utf-8')[3:].split("$")
		tempArray.remove('')
		print(tempArray)
		for peer in tempArray:
			ip, port = peer.split(":")
			peers.append((ip, int(port)))
		#while 1:
			#pass
	except:
		print("ERROR: YOU FUCKED UP")
		#while 1:
			#pass
	raw = ""
	listenThread = threading.Thread(target=listenOnSocket, args=(Tr, commandQueue))
	listenThread.start()
	print("Listener Started")

	print("Peers")
	print(peers)

	senderThread = threading.Thread(target=sendMessage, args=(Tr, peers, name))
	senderThread.start()
elif mode == 2:
	Tl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	Tr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	name = str(input("Enter Username:"))
	port = randrange(55556, 56555)
	print("Binding to port " + str(port))
	Tr.bind(('', port))
	Tl.bind(('', 12344))
	Tr.sendto(("test").encode('utf-8'), ("localhost", 12344))
	ownAddr = Tl.recvfrom(1024)
	print(ownAddr[0].decode('utf-8'))
	Tl.close()
	#peers.append(ownAddr[1])
	listenThread = threading.Thread(target=listenOnSocket, args=(Tr, commandQueue))
	listenThread.start()
	print("Listener Started")
	print("Sender Starting")
	senderThread = threading.Thread(target=sendMessage, args=(Tr, peers, name))
	senderThread.start()

#Command Queue Processing
while 1:
	while len(commandQueue) > 0:
		currentCommand = str(commandQueue[0])
		if currentCommand[:4] == "MSG&":
			#print("data is message: " + adjustedCommand)
			printToConsole(currentCommand[4:])
			commandQueue.pop(0)
		elif currentCommand[:1] == "%":
			processCommand(currentCommand, peers, Tr)
			commandQueue.pop(0)
		else:
			print(currentCommand)