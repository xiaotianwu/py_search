#!/usr/bin/python

import os
import sys
import threading
import time

from twisted.internet.fdesc import setNonBlocking
from twisted.internet.main import CONNECTION_LOST
from twisted.internet.main import CONNECTION_DONE
from twisted.internet.abstract import FileDescriptor

class AsyncFileReader(FileDescriptor):
    def __init__(self, fid, offset, length, bufLen = 8):
        self._fd = fid
        os.lseek(self._fd, offset, os.SEEK_SET)
        setNonBlocking(self._fd)
        self._readBufLen = bufLen
        self._readMaxLen = length
        self._readLen = 0
        self._allData = ''
        self.dataRecieved = AsyncFileReader.read_finish

    def fileno(self):
        return self._fd

    def connectionLost(self, args):
        print 'connectionLost'

    def doRead(self):
        print 'reading', self._readBufLen, 'bytes'
        data = os.read(self._fd, self._readBufLen)
        self._allData += data
        self._readLen += self._readBufLen
        print 'has read', self._readLen, 'bytes'
        if not data or self._readLen >= self._readMaxLen:
            self.dataRecieved(self, self._allData)
            return CONNECTION_LOST
    
    @staticmethod
    def read_finish(self, data):
        print 'finish reading', len(data)
        print 'allData =', data
        os.lseek(self._fd, 0, os.SEEK_SET)

class AsyncIOHandler:
    # global mapping for filename - fileObj pair
    # open the same file in different process is not permitted
    # TODO remove the above feature later
    __fileDescMapping = {}

    @staticmethod
    def read(fileName, offset = 0, length = 1024):
        if fileName not in AsyncIOHandler.__fileDescMapping:
            AsyncIOHandler.__fileDescMapping[fileName] = open(fileName, 'r')

        fileDesc = AsyncIOHandler.__fileDescMapping[fileName].fileno()
        reader = AsyncFileReader(fileDesc, offset, length)

        from twisted.internet import reactor
        reactor.addReader(reader)
        print 'add reader'
    
    @staticmethod
    def write(fileName, buf):
        pass

class AsyncIOThread(threading.Thread):
    def run(self):
        #AsyncIOHandler.read('test.txt')
        time.sleep(5)
        AsyncIOHandler.read('test.txt')
