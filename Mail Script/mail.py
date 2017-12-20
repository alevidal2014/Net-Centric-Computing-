#!/usr/bin/python

import os, codecs
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
import socket
import time
import re
import binascii

def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
    print "Sending ==> ", msg
    socket.send(msg + '\r\n')

def create_parsed(data):
    parsed = {}
    pairs = data.split('&')
    for pair in pairs:
        pairList = pair.split('=')
        nameDecode = decode(pairList[0])
        valueDecode = decode(pairList[1])
        parsed[nameDecode] = valueDecode
    return parsed

def decode(value):
    value = re.sub(r'[+]', ' ', value)
    return re.sub(r'%[0-9a-fA-F]{2}', convert_ascii, value)

def convert_ascii(match):
    match = match.group()
    return binascii.unhexlify(match[1:3])

def mail(mess):
    #Separating the message 
    #Original Format "GET /mail.py?from=avida059@fiu.edu&to=alevidal2014@gmail.com&subject=Hello&body=This is a test body&Submit=Send HTTP/1.1"
    
    #/mail.py?from=avida059@fiu.edu&to=alevidal2014@gmail.com&subject=Hello&body=This is a test body&Submit=Send
    fileString = message.split()[1]  
    #from=avida059@fiu.edu&to=alevidal2014@gmail.com&subject=Hello&body=This is a test body&Submit=Send
    parameters = fileString.partition("?")[2]  

    parsedString = create_parsed(parameters)
    mfrom = parsedString['from']
    mto = parsedString['to']
    msubject = parsedString['subject']
    mbody = parsedString['body']

    serverName = 'smtp.cis.fiu.edu'
    serverPort = 25

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    recv=send_recv(clientSocket, None, '220')

    clientName = 'Ale Vidal'

    userName= mfrom.partition("@")[0]
    userServer=mfrom.partition("@")[2]
    print userName
    print userServer

    toName=mto.partition("@")[0]
    toServer=mto.partition("@")[2]

    #Send HELO command and print server response.
    heloCommand='EHLO  %s' % clientName
    recvFrom = send_recv(clientSocket, heloCommand, '250')
    #Send MAIL FROM command and print server response.
    fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
    recvFrom = send_recv(clientSocket, fromCommand, '250')
    #Send RCPT TO command and print server response.
    rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
    recvRcpt = send_recv(clientSocket, rcptCommand, '250')
    #Send DATA command and print server response.
    dataCommand='DATA'
    dataRcpt = send_recv(clientSocket, dataCommand, '354')
    #Send message data.
    send(clientSocket, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
    send(clientSocket, "From: Ale Vidal <%s@%s>" % (userName, userServer));
    send(clientSocket, "Subject: %s" % msubject);
    send(clientSocket, "To: %s@%s" % (toName, toServer));
    send(clientSocket, ""); #End of headers

    send(clientSocket, mbody);    
   
    #Message ends with a single period.
    send_recv(clientSocket, ".", '250');
    #Send QUIT command and get server response.
    quitCommand='QUIT'
    quitRcpt = send_recv(clientSocket, quitCommand, '221')


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

        mail(message)

        f = open('confirmation.html', 'r')
        message2 = f.read()

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
