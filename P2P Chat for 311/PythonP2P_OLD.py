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
################################################################################################
class Mediator:
	seed()
	currentSwarm =[] #tuples of port/IP
	#checktime = clock() + 60
	medSocketL = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	medSocketS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	medSocketC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	def __init__(self, port, ip, medport):
		self.currentSwarm.append((ip, port))
		self.medSocketL.bind((ip, medport))
		self.medSocketC.bind((ip, medport - 1))
		threading.Thread(target=self.checkIn, args=(self.currentSwarm, ip, port)).start()
		threading.Thread(target=self.medListen, args=(1, 2)).start()
	def medConnect(self, rawTuple):
		connectorString = "%P_"
		swarmString = "%P_" + rawTuple[0] + ":" + str(rawTuple[1])
		for peer in self.currentSwarm:
			if (peer == ('localhost', 55554)):
				print("Skipping own address")
				continue
			connectorString = connectorString + peer[0] + ":" + str(peer[1]) + "$"
			self.medSocketS.sendto(swarmString.encode('utf-8'), (peer[0], peer[1]))
		self.medSocketS.sendto(connectorString.encode('utf-8'), (rawTuple[0], rawTuple[1]))
		self.currentSwarm.append(rawTuple)
	def checkIn(self, currentSwarm, ip, port):
		print("Entered CheckIn")
		while 1:
			#This part works
			sleep(45)
			print("Slept for 45 seconds")
			print(self.currentSwarm)
			#up to here
			for peer in self.currentSwarm:
				if (peer == (ip, port)):
					print("Skipping own address")
					continue
				self.medSocketS.sendto(("%A_" + ip + ":" + str(port)).encode('utf-8'), peer)
				self.medSocketC.settimeout(2)
				print("Trying " + peer[0] + ":" + str(peer[1]))
				try: #wait for timeout
					raw = self.medSocketC.recvfrom(1024) #if you get a reply, do nothing
					print(raw[0].decode('utf-8'))
					print("Got a reply from " + raw[1][0] + ":" + str(raw[1][1]))
				except: #if you don't get a reply, tell everyone the peer is gone
					print("Peer's gone yo")
					pass
					self.currentSwarm.remove(peer)
					print("Deleted a peer" + peer[0] + ":" + str(peer[1]))
					for peer2 in self.currentSwarm:
						if (peer2 == (ip, port)):
							print("Skipping own address")
							continue
						#tell everyone else to drop the guy
						print("Sending Drop Message to " + peer2[0] + ":" + str(peer2[1]))
						self.medSocketS.sendto(("%D_" + peer[0] + ":" + str(peer[1])).encode('utf-8'), peer2)
	def medListen(self,a, b):
		while 1:
			try:
				raw = self.medSocketL.recvfrom(1024)
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
################################################################################################
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
			returned.append(str(data))

#Functions for processing input from socket
def processCommand(command, peers, socket):
	if command[:3] == "%P_":
		addPeer(command[3:], peers)
	elif command[:3] == "%D_":
		removePeer(command[3:], peers)
	elif command[:3] == "%A_":
		confirmAlive(command[3:], socket)
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
	ip, port = data.split(":")
	newTuple = (ip, int(port))
	socket.sendto(("%A_").encode('utf-8'), newTuple)
def printToConsole(data):
	print("\r" + "                                          " + "\r" + data)
	rePrompt()
#Fucktions for sending things
def sendMessage(S, peers, name):
	while 1:
		message = input("<" + name + ">")
		message = "<" + name + ">" + message
		for peer in peers:
			S.sendto(message.encode('utf-8'), (peer))
#Create Mediator object to listen on port 55555
###############################################
####################END DEFS###################
###############################################
try:
	Mediator(55554, "localhost", 55555)
except:
	print("Mediator Already Active")
#Temp socket
Tl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#registered Socket
Tr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
peers = [] #tuples of all peer addresses
commandStack = [] #stores actions to be processed in main thread
name = str(input("Enter Username:"))
ip = str(input("Enter IP of Mediator:"))
#necessary to receive from mediator
port = 12345
#bind socket for listening
Tl.bind(('localhost', port))

#Very Temporary code
#Send a request for new port
Tl.sendto(("%S_").encode('utf-8'), (ip, 55555))
raw = Tl.recvfrom(1024)
port = int(raw[0].decode('utf-8'))
#Print some debug info (message ip:port)
print (raw[0].decode('utf-8') + " " + raw[1][0] + ":" + str(raw[1][1]))
Tl.close()
#bind Tr to approved port
Tr.bind(('', port))
#request list of peers
Tr.sendto(("%C_").encode('utf-8'), (ip, 55555))
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
listenThread = threading.Thread(target=listenOnSocket, args=(Tr, commandStack))
listenThread.start()
print("Listener Started")

print("Peers")
print(peers)

senderThread = threading.Thread(target=sendMessage, args=(Tr, peers, name))
senderThread.start()

while 1:
	while len(commandStack) > 0:
		currentCommand = str(commandStack[0])
		if currentCommand[:4] == "MSG&":
			#print("data is message: " + adjustedCommand)
			printToConsole(currentCommand[4:])
			commandStack.pop(0)
		elif currentCommand[:1] == "%":
			processCommand(currentCommand, peers, Tr)
			commandStack.pop(0)