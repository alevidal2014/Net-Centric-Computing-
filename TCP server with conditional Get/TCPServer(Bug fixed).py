#TCPServer.py

import os, codecs
from datetime import datetime
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort=14001 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print "Interrupt with CTRL-C"

while True:
    try:
        lastModSince = 1;
        #Date object of the last modifieddate of the server
        serverModifyDate_object = datetime.strptime('30 Oct 2017 8:24:52', '%d %b %Y %H:%M:%S')

        connectionSocket, addr = serverSocket.accept()
        print "Connection from %s port %s\n" % addr  
        # Receive the client packet 
        message = connectionSocket.recv(2048)
        print message
        
        #if not message:
           # print"Server Closed"
            #connectionSocket.close()
            #break

        if message:
            filename = message.split()[1].partition("/")[2]

            #Checking the Conditional Get headers
            sinceIndex = message.find("If-Modified-Since:", 0, len(message))
            print sinceIndex

            if sinceIndex != -1:
                sinceline = message[sinceIndex:len(message)].split('\n')[0]
                sincelist = sinceline.partition(",")[2].partition["GMT"][0]
                clientDateObject = datetime.strptime(sincelist , ' %d %b %Y %I:%M:%S')
                lastModSince = (clientDateObject < serverModifyDate_object)

            #Checking the Accepted languages headers
            lanIndex = message.find("Accept-Language:", 0, len(message))
            lanline = message[lanIndex:len(message)].split('\n')[0]
            lanlist = lanline.split()[1].split(",")
        
            for l in lanlist:
                if l.find("en")!= -1:
                    exFile = '.en'
                    break
                elif l.find("es")!= -1:
                    exFile = '.es'
                    break
                elif l.find("de")!= -1:
                    exFile = '.de'
                    break

            file = open(filename+exFile, 'rU').read()
            filesize = os.path.getsize(filename+exFile)

            if lastModSince:
                connectionSocket.send('HTTP/1.1 200 OK\r\n')
                connectionSocket.send('Connection: closed\r\n')
                connectionSocket.send('Content-Length: %d\r\n'% filesize)
                connectionSocket.send('Content-Type: text/html\r\n')
                connectionSocket.send('Cache-Control: max-age=120\r\n')
                connectionSocket.send('Last-Modified: Wed, 30 Oct 2017 8:24:52 GMT\r\n')
                connectionSocket.send('Accept-language: en, es, de\n\n')
                connectionSocket.send(file)
                connectionSocket.close()
            else:
                connectionSocket.send('HTTP/1.x 304 Not Modified\r\n') 
                connectionSocket.send('Content-Type: text/html\r\n')
                connectionSocket.send('Last-Modified: Wed, 30 Oct 2017 8:24:52 GMT\r\n')
                connectionSocket.send('Accept-language: en, es, de\n\n')
                connectionSocket.send('This is 304 message')
                connectionSocket.close()

    except IOError:
	#404 errorPage.html declared on same folder
	#based on sourcePage
        f = open('errorPage.html', 'r')
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

serverSocket.close()