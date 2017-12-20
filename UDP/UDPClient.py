#UDPClient.py
from socket import socket, SOCK_DGRAM, AF_INET
import datetime

serverName = 'localhost'
serverPort = 14001
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowercase sentence: ')
send_time_ms = datetime.datetime.now()
clientSocket.sendto(message, (serverName, serverPort))

clientSocket.settimeout(1)
modifiedMessage =""
try:
	modifiedMessage, addr = clientSocket.recvfrom(2048)
	recv_time_ms = datetime.datetime.now()
	rtt_in_ms = recv_time_ms.microsecond - send_time_ms.microsecond
	#print modifiedMessage, addr
	print "\nClient's IP address: " , addr
	print 'Modified Message from the server: %s' % modifiedMessage
	print 'The RTT was: %d ms' % rtt_in_ms
   
except:
 	if not modifiedMessage:
		print "Waiting Time out after 1 sec"

clientSocket.close()