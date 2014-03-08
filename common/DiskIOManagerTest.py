#!/usr/bin/python

import os
import time
#import gevent
import threading

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

def CreateTestData(fileNum):
    os.system('mkdir testdata')
    for i in range(0, fileNum):
        fileName = 'testdata/testFile' + str(i)
        print('create ' + fileName)
        os.system('dd of=' + fileName + ' if=/dev/zero bs=1024 count=1024')

def DeleteTestData():
    os.system('rm testdata -r')  

if __name__ == '__main__':
    fileNum = 10
    CreateTestData(fileNum)    

    dmThread = DiskIOManagerTestThread()
    dmThread.start()
    
    #manager = DiskIOManager()
    #gevent.spawn(manager.run)

    events = []

    for i in range(0, fileNum):
        req = DiskIORequest(i, 'READ', 'testdata/testFile' + str(i),
                            0, -1)
        ev = dmThread.PostDiskIORequest(req)
        #ev = manager.PostDiskIORequest(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    print('all done')

    #manager.PostStopRequest()
    dmThread.PostStopRequest()

    #gevent.sleep(5)
    time.sleep(5)

    DeleteTestData()
