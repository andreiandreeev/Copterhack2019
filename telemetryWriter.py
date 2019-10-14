
import socket
import math

#Define transmission information
UDP_IP   = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#Init node

while True:

	#Send all the information
	sock.sendto('gneg', (UDP_IP, UDP_PORT))






