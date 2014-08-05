#!/usr/bin/env python

import os, socket, threading, SocketServer, sys

class ThreadedRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
	self.server.addClient(self)

    def handle(self):
	while True:
	    data = self.request.recv(10240)
	    if data != "":
		self.server.sendToOthers(data, self)
	    else:
		print "Connection closed"
		return

    def finish(self):
	self.server.removeClient(self)

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.UnixStreamServer):
    def __init__(self, server_address, RequestHandlerClass):
	try:
	    os.unlink(server_address)
	except OSError:
	    if os.path.exists(server_address):
		raise
	SocketServer.UnixStreamServer.__init__(self, server_address, RequestHandlerClass)
        self.clients = []

    def addClient(self, c):
        self.clients.append(c)
	print "Added new client - I now have %d clients" % len(self.clients)

    def removeClient(self, c):
        self.clients.remove(c)
	print "Removed client - I now have %d clients" % len(self.clients)

    def sendToOthers(self, msg, me):
        for c in self.clients:
            if c != me:
		c.request.sendall(msg)

    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <socketname>" % sys.argv[0]
	sys.exit(1)

    server = ThreadedServer(sys.argv[1], ThreadedRequestHandler)
    print "Starting Unix Domain Socket hub called '%s'" % sys.argv[1]
    server.serve_forever()

