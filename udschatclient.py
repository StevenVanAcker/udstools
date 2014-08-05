#!/usr/bin/env python

import sys
import time
import asyncore, socket

class Client(asyncore.dispatcher):
    def __init__(self, sockname):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.connect(sockname)
        print "Client Start..."

    def handle_close(self):
        print "Client: Connection Closed"
        self.close()

    def handle_read(self):
        data = self.recv(1024)
        if data:
            print "Received ", data


class CmdlineClient(asyncore.file_dispatcher):
    def __init__(self, sender, file):
        asyncore.file_dispatcher.__init__(self, file)
        self.sender = sender

    def handle_read(self):
 	data = self.recv(1024)
        self.sender.send(data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <socketname>" % sys.argv[0]
        sys.exit(1)

    sender = Client(sys.argv[1])
    cmdline = CmdlineClient(sender, sys.stdin)
    asyncore.loop()
