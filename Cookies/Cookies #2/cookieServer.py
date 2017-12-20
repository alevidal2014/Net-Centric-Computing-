#cookieServer.py

import os, codecs
from datetime import datetime
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort=14007 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print "Interrupt with CTRL-C"

while True:
    try:
        lastModSince = 1;
        #Date object of the last modifieddate of the server
        #serverModifyDate_object = datetime.strptime('30 Oct 2017 8:24:52', '%d %b %Y %H:%M:%S')

        connectionSocket, addr = serverSocket.accept()
        print "Connection from %s port %s\n" % addr  
        # Receive the client packet 
        message = connectionSocket.recv(4096)
        print message
        
        #if not message:
           # print"Server Closed"
            #connectionSocket.close()
            #break

        if message:
            filename = message.split()[1].partition("/")[2]
            f = open(filename, 'r')
            finalMessage = f.read()

            '''#Checking the Conditional Get headers
            sinceIndex = message.find("If-Modified-Since:", 0, len(message))
            print sinceIndex

            if sinceIndex != -1:
                sinceline = message[sinceIndex:len(message)].split('\n')[0]
                sincelist = sinceline.partition(",")[2].partition["GMT"][0]
                clientDateObject = datetime.strptime(sincelist , ' %d %b %Y %I:%M:%S')
                lastModSince = (clientDateObject < serverModifyDate_object)'''

            #Checking the Accepted languages headers
            cookieIndex = message.find("Cookie:", 0, len(message))
            
            if cookieIndex != -1:
            	cookieline = message[cookieIndex:len(message)].split('\n')[0]
            	#print "\nThis is the cookie Line: " + cookieline +"\n"
            	cookielist = cookieline.split(";")
            	cookieMessage = "";
            	
            	for c in cookielist:
            		cookieMessage += c + "\n"

            	#print "\nThis is the cookie Message: " + cookieMessage +"\n"
            	f1 = open('cookie1.html', 'r')
            	message2 = f1.read()
            	f2 = open('cookie2.html', 'r')
            	message3 = f2.read()
            	finalMessage = message2 + cookieMessage + message3

            #filesize = os.path.getsize(finalMessage)
            

            if lastModSince:
                connectionSocket.send('HTTP/1.1 200 OK\r\n')
                connectionSocket.send('Connection: closed\r\n')
                #connectionSocket.send('Content-Length: %d\r\n'% filesize)
                connectionSocket.send('Content-Type: text/html\r\n')
                connectionSocket.send('Cache-Control: max-age=21600\r\n')
                connectionSocket.send('Last-Modified: Wed, 30 Oct 2017 8:24:52 GMT\r\n')
                connectionSocket.send('Etag: 4135cda4\r\n')
                connectionSocket.send('Accept-language: en, es, de\n\n')
                connectionSocket.send(finalMessage)
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