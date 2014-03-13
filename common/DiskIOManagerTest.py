#!/usr/bin/python

import os
import random
#import gevent
import threading

from plain_file.PlainFile import PlainFileIORequest
from uncompress_index.UncompressIndex import UncompressIndexIORequest
from uncompress_index.UncompressIndex import UncompressIndexWriter
from uncompress_index.UncompressIndex import UncompressIndex
from DiskIOManager import DiskIOManagerThread

def CreateTestData1(begin, end):
    os.system('mkdir testdata')
    for i in range(begin, end):
        fileName = 'testdata/testFile' + str(i)
        print('create ' + fileName)
        os.system('dd of=' + fileName + ' if=/dev/zero bs=1024 count=1024')

def CreateTestData2(begin, end):
    for i in range(begin, end):
        fileName = 'testdata/testFile' + str(i)
        print('create ' + fileName)
        with open(fileName, 'w') as f:
            f.write('abcdefghijklmnopqrstuvwxyz')

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

def CreateTestData3(begin, end):
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
    dmThread = DiskIOManagerThread(4)
    dmThread.start()
    
    events = []
    CreateTestData1(0, 10)    

    #manager = DiskIOManager()
    #gevent.spawn(manager.run)

    for i in range(0, 10):
        req = PlainFileIORequest('READ',
                                 'testdata/testFile' + str(i),
                                 0, -1)
        ev = dmThread.PostIORequest(req)
        #ev = manager.PostIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    print('test round 1 all done')

    events = []
    CreateTestData2(10, 30)
    requests = []

    for i in range(10, 30):
        req = PlainFileIORequest('READ',
                                 'testdata/testFile' + str(i),
                                 i, i)
        requests.append(req)
        ev = dmThread.PostIORequest(req)
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

    for i in range(30, 20000):
        req = UncompressIndexIORequest('READ',
                                       'testdata/testFile' + str(i % 20 + 30),
                                       random.randint(0, 9999))
        requests.append(req)
        ev = dmThread.PostIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    for req in requests:
        assert req.result == randomIndex.Fetch(req.termId)

    print('test round 3 all done')
    DeleteTestData()

    #manager.PostStopRequest()
    dmThread.PostStopRequest()
    dmThread.join()
