# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Spencer
#   Date:   9/24/2014
# - - - - - - - - - - - - - - - - - - - - - -

#Import modules for client
import socket
import threading
import sys
import random
#Function for prompt used in listener
def console_message(message):
	print("-->" + message)
def prompt():
    sys.stdout.write(name + ": ")
    sys.stdout.flush()
#Function to listen for messages from server, runs on its own thread
def listen_for_message():
	bad_dc = False
	while running:
		try:
			data = client_socket.recv(1024).decode('utf-8')
		except:
			bad_dc = True
			print("<ABORTED>")#aligns the console messages
			console_message("Error, socket to server has closed")
			client_socket.close()
			break
		#Check for kill codes
		if (data == "%%INV_UNAME"):
			break
		elif (data != "%%null"):
			print ("\r" + "                                        " + "\r" + data)
			prompt()
	console_message("Listener Exiting")
	if bad_dc:
		console_message("Press Enter to reconnect...")
#Set a variable to let the listener know we're working
running = True
#Make the listener object
listener = threading.Thread(target=listen_for_message, args=(), daemon=False)
#create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#get info for connection
name = input("Enter Username: ")
if (name==""):
	name = ("DefaultUser" + str(random.randint(1, 1000)))
	print('defaulted to ' + name)
ip = input("Enter IP: ")
if (ip==""):
	ip = "localhost"
	print('defaulted to localhost')
port = input("Enter Port: ")
if (port==""):
	port = "55555"
	print('defaulted to 55555')
#First time setup
#connect socket
while 1:
	#try to connect
	try:
		client_socket.connect((str(ip), int(port)))
		#if it works you can break the loop
		break
	except:
		#if it can't connect, try to get new info (until you can connect)
		console_message("Cannot Connect")
		console_message("Re-enter connection info")
		ip = input("Enter IP: ")
		if (ip==""):
			ip = "localhost"
			print('defaulted to localhost')
		port = input("Enter Port: ")
		if (port==""):
			port = "55555"
			print('defaulted to 55555')
#Start the listener (this is as good a time as any
listener.start()
#main process loop, goes forever until terminal is closed
while 1:
	print("-------------------")
	#First thing sent will be the username
	data = name
	#Loop until broken, easier this way for general testing
	while listener.isAlive():
		if (data != ""):
			try:
				client_socket.send(data.encode('utf-8'))
			except:
				console_message("Data could not be sent, bad socket")
				break
			data = ""
		data = input(name + ": ")
		#If the exit command is given, exit the room
		if (data == "/exit"):
			break
	#This switches off the listener
	running = False
	#Send Terminate message
	try:
		client_socket.send(("%%TERMINATE").encode('utf-8'))
	except:
		pass
	listener.join()
	console_message("Listener Thread Joined")
	#Look for the Terminate OK
	try:
		data = client_socket.recv(128).decode('utf-8')
	except:
		pass
	if (data == "DC OK*"):
		#close and end the socket
		client_socket.close()
		console_message("Connection Closed")
	#####################################
	#loop will allow client to reconnect#
	#####################################
	#allow the listener to loop successfully again
	running = True 
	#remake the listener thread
	listener = threading.Thread(target=listen_for_message, args=(), daemon=False)
	#Get new connection data
	print("Enter New Connection Data")
	ip = input("Enter IP: ")
	if (ip==""):
		ip = "localhost"
		print('defaulted to localhost')
	port = input("Enter Port: ")
	if (port==""):
		port = "55555"
		print('defaulted to 55555')
	#remake socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#connect socket (same as initial code)
	while 1:
		try:
			client_socket.connect((str(ip), int(port)))
			break
		except:
			console_message("Cannot Connect")
			console_message("Re-enter connection info")
			ip = input("Enter IP: ")
			if (ip==""):
				ip = "localhost"
				print('defaulted to localhost')
			port = input("Enter Port: ")
			if (port==""):
				port = "55555"
				print('defaulted to 55555')
	#Start the listener
	listener.start()