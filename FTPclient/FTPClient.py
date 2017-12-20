#FTPClient.py
#!/usr/bin/python

import os, codecs
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
import socket
import time
import re
import binascii

from ast import literal_eval

def send(socket, msg): 
	print "===>sending: " + msg
	socket.send(msg + "\r\n")
	recv = socket.recv(1024)
	print "<===receive: " + recv
	return recv

def ftprequest(mess):
	serverName = 'ftp.swfwmd.state.fl.us'
	serverPort = 21
	clientSocket = socket.socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	condition = True
	message = clientSocket.recv(2048)
	print message
	while condition:
		message = clientSocket.recv(2048)
		print message
		condition = message[0:6] != "220---"
	message = send(clientSocket,"USER Anonymous")
	message = send(clientSocket,"PASS avida059@cs.fiu.edu")
	message = send(clientSocket,"TYPE A")
	message = send(clientSocket,"PASV")
	start = message.find("(")
	end  = message.find(")")
	tuple = message[start+1:end].split(',')
	print tuple
	#build the port from the last two numbers
	port = int(tuple[4])*256 + int(tuple[5])
	print port
	dataSocket = socket.socket(AF_INET, SOCK_STREAM)
	dataSocket.connect((serverName, port))

	if mess== "root":
		message = send(clientSocket,"LIST")
	else:
		message = send(clientSocket,"RETR"+mess)

	returnMess = dataSocket.recv(2048)
	print returnMess
	message = clientSocket.recv(2048)
	print message
	dataSocket.close()
	message = send(clientSocket,"QUIT")
	clientSocket.close()
	return returnMess



#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
TcpserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TcpserverPort=14002 
TcpserverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Assign IP address and port number to socket
TcpserverSocket.bind(('', TcpserverPort))
TcpserverSocket.listen(1)
print "Interrupt with CTRL-C"

while True:
    try:
        connectionSocket, addr = TcpserverSocket.accept()
        print "Connection from %s port %sn" % addr  
        # Receive the client packet 
        message = connectionSocket.recv(2048)
        print message
        if not message:
            print"Server Closed"
            connectionSocket.close()
            break

        result = ftprequest(message)

        f1 = open('ftpc1.html', 'r')
        message2 = f1.read()
        f2 = open('ftpc2.html', 'r')
        message3 = f2.read()

        message2 = message2 + result + message3

        print message2

        connectionSocket.send('HTTP/1.1 404 Not Found\r\n')
        connectionSocket.send('Connection: closed\r\n')
        connectionSocket.send('Content-Type: text/html\n\n')

        connectionSocket.send(message2)
        #print "Not Found %s" % filename
        #sendError(connectionSocket, '404', 'Not Found')
        connectionSocket.close()

        break
        
    except IOError:
    #404 errorPage.html declared on same folder
    #based on sourcePage
        f = open('../TCPserver/errorPage.html', 'r')
        message2 = f.read()

        connectionSocket.send('HTTP/1.1 404 Not Found\r\n')
        connectionSocket.send('Connection: closed\r\n')
        connectionSocket.send('Content-Type: text/html\n\n')

        connectionSocket.send(message2)
        #print "Not Found %s" % filename
        #sendError(connectionSocket, '404', 'Not Found')
        connectionSocket.close()
    except KeyboardInterrupt:
        print "\nInterrupted by CTRL-C"
        break

TcpserverSocket.close()	
