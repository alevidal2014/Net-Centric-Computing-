#TCPServer.py

import os, codecs
from datetime import datetime
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR

def as_client(serverName):
    print "Inside method"
    #print serverName
    serverName = serverName.split('%2F')[2]
    print serverName
    if(serverName == "www.youtube.com" or serverName == "www.bing.com" ):
        website = "Error"
    else:        
        serverPort = 80
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        string_request = "GET /https://" + serverName + "/ HTTP/1.1\r\n"
        string_request += "Host: fiu.edu\r\n"
        string_request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0\r\n"
        string_request += "Accept: text/html\n\n"
        print string_request;
        clientSocket.send(string_request)
        #clientSocket.sendall("GET /\r\n")
        website = clientSocket.recv(8192)
        clientSocket.close()
    
    return website
        

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
        
        connectionSocket, addr = serverSocket.accept()
        print "Connection from %s port %s\n" % addr  
        # Receive the client packet 
        message = connectionSocket.recv(2048)
        print message
        
        if message:
            filename = message.split()[1].partition("/")[2]
            url = filename.partition("=")[2]
            print url
                        
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

            web = as_client(url)            
            print web
            if(web == "Error"):
                f = open('errorPage.html', 'r')
                message2 = f.read()

                connectionSocket.send('HTTP/1.1 404 Not Found\r\n')
                connectionSocket.send('Connection: closed\r\n')
                connectionSocket.send('Content-Type: text/html\n\n')

                connectionSocket.send(message2)
                #print "Not Found %s" % filename
                #sendError(connectionSocket, '404', 'Not Found')
                connectionSocket.close()
                break;

            #connectionSocket.send('HTTP/1.1 200 OK\r\n')
            #connectionSocket.send('Connection: closed\r\n')
            #connectionSocket.send('Content-Type: text/html\n\n')
            connectionSocket.send(web)
            
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