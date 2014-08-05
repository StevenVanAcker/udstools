#!/usr/bin/env python

import sys, socket, os

def usage():
    print
    print "Usage: %s [fdspec ...] -- <command> <args>" % sys.argv[0]
    print "  fdspec = fd:filename"
    print "    e.g. 99:/tmp/sock will open unix socket /tmp/sock and connect it to filedescriptor 99"
    print "  Example usage: %s 99:/tmp/sock -- kvm ... -net socket,fd=99 -net nic"
    print

def connectFilenoToUnixSocket(fd, sockname):
    sockfd = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sockfd.connect(sockname)
    os.dup2(sockfd.fileno(), fd) # rename socket
    sockfd.close()

splitsymbol = "--"

if not splitsymbol in sys.argv:
    usage()
    sys.exit(1)

splitter = sys.argv.index(splitsymbol)

myargs = sys.argv[1:splitter]
restargs = sys.argv[splitter+1:]

for a in myargs:
    (fds, sockname) = a.split(":")
    connectFilenoToUnixSocket(int(fds), sockname)

os.execvp(restargs[0], restargs)
