#!/usr/bin/python

import os
import random
import time
#import gevent
import threading

from plain_file_dealer.PlainFile import PlainFileIORequest
from uncompress_index_dealer.UncompressIndex import UncompressIndexIORequest
from uncompress_index_dealer.UncompressIndex import UncompressIndexWriter
from uncompress_index_dealer.UncompressIndex import UncompressIndex
from DiskIOManager import *

class DiskIOManagerTestThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._manager = DiskIOManager()

    def run(self):
        self._manager.Run() 

    def PostDiskIORequest(self, request):
        return self._manager.PostDiskIORequest(request)

    def PostStopRequest(self):
        self._manager.PostStopRequest()

def CreateTestData1(begin, end):
    os.system('mkdir testdata')
    for i in range(begin, end):
        fileName = 'testdata/testFile' + str(i)
        print('create ' + fileName)
        os.system('dd of=' + fileName + ' if=/dev/zero bs=1024 count=1024')

def CreateTestData2(begin, end):
    os.system('mkdir testdata')
    for i in range(begin, end):
        fileName = 'testdata/testFile' + str(i)
        print('create ' + fileName)
        with open(fileName, 'w') as f:
            f.write('abcdefghijklmnopqrstuvwxyz')

def GenRandomIndex():
    i = 0
    s = set()
    while i < 100:
        (item1, item2) = (random.randint(0, 10000),
                          random.randint(0, 10000))
        if (item1, item2) in s:
            continue
        else:
            s.add((item1, item2))
            i += 1
    return s

def CreateTestData3(begin, end):
    os.system('mkdir testdata')
    index = UncompressIndex()
    for i in range(0, 10000):
        index.Add(i, GenRandomIndex())

    for i in range(begin, end):
        fileName = 'testdata/testFile' + str(i)
        print('create index file' + fileName)
        writer = UncompressIndexWriter()
        writer.Write(index, fileName)

    return index

def DeleteTestData():
    os.system('rm testdata -r')  

if __name__ == '__main__':
    dmThread = DiskIOManagerTestThread()
    dmThread.start()
    
    events = []
    CreateTestData1(0, 10)    

    #manager = DiskIOManager()
    #gevent.spawn(manager.run)

    for i in range(0, 10):
        req = PlainFileIORequest(i, 'READ',
                                 'testdata/testFile' + str(i),
                                 0, -1)
        ev = dmThread.PostDiskIORequest(req)
        #ev = manager.PostDiskIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    print('test round 1 all done')

    events = []
    CreateTestData2(10, 30)
    requests = []

    for i in range(10, 30):
        req = PlainFileIORequest(i, 'READ',
                                 'testdata/testFile' + str(i),
                                 i, i)
        requests.append(req)
        ev = dmThread.PostDiskIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    string = 'abcdefghijklmnopqrstuvwxyz'
    j = 10
    for req in requests:
        assert req.offset == j
        assert req.length == j
        assert req.result == string[j:j + j]
        j += 1

    print('test round 2 all done')

    events = []
    randomIndex = CreateTestData3(30, 50)
    requests = []

    for i in range(30, 50):
        req = UncompressIndexIORequest(i, 'READ',
                                       'testdata/testFile' + str(i),
                                       random.randint(0, 99))
        requests.append(req)
        ev = dmThread.PostDiskIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    for req in requests:
        assert req.result == randomIndex.Fetch(req.termId)

    print('test round 3 all done')
    DeleteTestData()

    #manager.PostStopRequest()
    dmThread.PostStopRequest()

    #gevent.sleep(2)
    time.sleep(2)
