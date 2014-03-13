#!/usr/bin/python

import os
import random
import shutil
#import gevent
import threading

from IORequestType import IORequest
from uncompress_index.UncompressIndex import UncompressIndexWriter
from uncompress_index.UncompressIndex import UncompressIndex
from DiskIOManager import DiskIOManagerThread

def GenRandomIndex():
    i = 0
    s = set()
    while i < 1000:
        (item1, item2) = (random.randint(0, 10000),
                          random.randint(0, 10000))
        if (item1, item2) in s:
            continue
        else:
            s.add((item1, item2))
            i += 1
    return s

def CreateTestData(begin, end):
    if os.path.exists('testdata'):
        shutil.rmtree('testdata')
    os.mkdir('testdata')
    index = UncompressIndex()
    for i in range(0, 10000):
        index.Add(i, GenRandomIndex())

    fileNameBase = 'testdata/testFile' + str(begin)
    print('create index file' + fileNameBase)
    writer = UncompressIndexWriter()
    writer.Write(index, fileNameBase)

    for i in range(begin + 1, end):
        fileName = 'testdata/testFile' + str(i)
        cp = 'cp ' + fileNameBase + ' ' + fileName
        os.system(cp)

    return index

def DeleteTestData():
    os.system('rm testdata -r')  

if __name__ == '__main__':
    randomIndex = CreateTestData(0, 10)

    #manager = DiskIOManager()
    #gevent.spawn(manager.run)
    dmThread = DiskIOManagerThread(4, 5000)
    #dmThread = DiskIOManagerThread(4, 0)
    dmThread.start()
    
    events = []
    requests = []

    for i in range(0, 50000):
        fileName = 'testdata/testFile' + str(i % 10)
        req = IORequest('READ', fileName,
                        random.randint(0, 9999))
        requests.append(req)
        ev = dmThread.PostIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    for req in requests:
        assert req.result == randomIndex.Fetch(req.key)

    print('test all done')
    DeleteTestData()
    
    #manager.PostStopRequest()
    dmThread.PostStopRequest()
    dmThread.join()

    print 'Cache Hit Ratio:', dmThread._manager.CacheHitRatio()
