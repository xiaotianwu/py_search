#!/usr/bin/python

from AsyncIO import AsyncIOThread

thread = AsyncIOThread()
thread.start()

from twisted.internet import reactor
print 'start running'
reactor.run()
