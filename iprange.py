#!/usr/bin/env python
import os, sys, re, time
from threading import Thread

class testit(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1

def run(self):
    """ The actual ping of the IP

    Returns:
        The result of the ping command.
    """
    pingaling = os.popen('ping -q -c2 ' + self.ip,'r')
    while 1:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(testit.lifeline,line)
        if igot:
            self.status = int(igot[0])

if __name__ == '__main__' or __name__ == sys.argv[0]:
    testit.lifeline = re.compile(r'(\d) received')
    report = ('No response', 'Partial Response', 'Alive')

    print time.ctime()

    pinglist = []

    for host in xrange(1,9):
        ip = '192.168.0.' + str(host)
        current = testit(ip)
        pinglist.append(current)
        current.start()

    for pingle in pinglist:
        pingle.join()
        if report[pingle.status] != 'No response':
             print 'Status from %s is %s' % (pingle.ip, report[pingle.status])

    print time.ctime()
