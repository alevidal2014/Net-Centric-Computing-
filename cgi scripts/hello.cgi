#!/usr/bin/python
import sys
import os
sys.stderr = sys.stdout
print "Content-type: text/plain\n"


print "Name: Alejandro Vidal\n"

print "Requesting Headers..."
print "REMOTE_USER:\t\t" + os.environ["REMOTE_USER"]
print "HTTP_ACCEPT:\t\t" + os.environ["HTTP_ACCEPT"]
print "HTTP_ACCEPT_LANGUAGE:\t" + os.environ["HTTP_ACCEPT_LANGUAGE"]
if os.environ["QUERY_STRING"] == "":
	print "QUERY_STRING:\t\tThe Query String is empty."
else:
	print "QUERY_STRING:\t\t" + os.environ["QUERY_STRING"]
print "HTTP_USER_AGENT:\t" + os.environ["HTTP_USER_AGENT"]
print "REQUEST_METHOD:\t\t" + os.environ["REQUEST_METHOD"]


