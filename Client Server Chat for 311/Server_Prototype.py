# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Spencer
#   Date:   9/24/2014
# - - - - - - - - - - - - - - - - - - - - - -

#Import the important Python modules
import socket
import threading
#set up the listening socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#TODO: Add options for server config including port and IP
s_ip = input("Enter Server IP (blank for local): ")
s_port = input("Enter Server port (blank for default): ")
if s_port == "":
	s_port = 55555
s_port = int(s_port)
serversocket.bind((str(s_ip), s_port))
serversocket.listen(5)
#print some output
print("Chat Server is now active. Press control-C to exit.")
print("Awaiting initial connection...")
#define some arrays for various things
connections = []
returned = []
currentusers = []
#Function to pass messages to clients that didn't send them
def echoback(connect, conlist, message):
	for each in connections:
		if (each != connect):#skip the client that sent the message
			each.send(message.encode('utf-8'))
#Function to get the list of currently online users
def getnamelist(connect):
	ulist = ""
	if (len(currentusers) > 0):#Obviously, only get the list if it actually exists
		ulist = ulist + "Current User List:\n"
		for each in currentusers:
			ulist = ulist + each + "\n"
		ulist = ulist + "-------------------"
		connect.send(ulist.encode('utf-8'))
#Function to process any incoming connections, runs on its own thread
def process_incoming_conn(serversocket, returned):
	while 1:
		returned_ = serversocket.accept()#accept all incoming
		returned.append(returned_)#Put the values of accept() into an array for processing on the main thread
threading.Thread(target=process_incoming_conn, args=(serversocket, returned)).start()
#Client thread function, runs on its own thread obviously
def client_threading(connect, ip, port, conlist):
	#First, get the first message from the client
	#Currently this is the username
	buffer = connect.recv(256).decode('utf-8')
	clientname = str(buffer)
	#Make sure only one person can use each username at once
	for each in currentusers:
		if (clientname==each):
			connect.send(("Error: Username already in use.").encode('utf-8'))
			connect.send(("%%INV_UNAME").encode('utf-8'))
			connections.remove(connect)
			connect.close()
			print("Client thread for " + clientname + " terminated.")
			return
	#Tell everyone there's a new user
	echoback(connect, conlist, (str(buffer) + " has entered the room."))
	#Add joiner to the list of users
	currentusers.append(str(buffer))
	#display all users in the room
	getnamelist(connect)
	print(str(buffer) + " added to session")
	while 1:
		#Read user input
		try:
			buffer = connect.recv(1024).decode('utf-8')
		except:
			#If the client forcibly disconnects, do this
			print("Error, Client (" + clientname + ") Socket Invalid")
			connections.remove(connect)
			echoback(connect, conlist, (clientname + " has left the room."))
			currentusers.remove(clientname)
			connect.close()
			break
		if buffer:
			#If the user is terminating their connection
			if (str(buffer) == "%%TERMINATE"):
				connect.send(("%%null").encode('utf-8')) #Send one message to hit the listener and stop it
				connect.send(("DC OK*").encode('utf-8')) #Send a message to the client that you're ready to DC
				#remove user from connection list
				connections.remove(connect)
				print(clientname + " removed from session")
				print("Connection closing")
				#give leave message
				echoback(connect, conlist, (clientname + " has left the room."))
				#remove user from current users list
				currentusers.remove(clientname)
				break
			#Server log message for received message
			print(str(ip)+":"+str(port) +" ("+ clientname +") " + " sent: " + buffer)
			message = str(buffer)
			print("Echoing to clients...")
			echoback(connect, conlist, (clientname + ": " + message))
	print("Client thread for " + clientname + " terminated.")
while 1:
	#If there's some new connection to be processed, so some stuff
	while (len(returned) > 0):
		#Split up the values
		con_obj, address = returned[0]
		(ip_, port_) = address
		#Add the connection object to an array
		connections.append(con_obj)
		#Pop the Object to be processed off the stack
		returned.pop(0)
		print("Adding thread for new connection")
		#Thread a new client
		threading.Thread(target=client_threading, args=(con_obj, ip_, port_, connections)).start()
#You'll never actually see this
print("Server socket closing...")
#Closing the socket
serversocket.close()
