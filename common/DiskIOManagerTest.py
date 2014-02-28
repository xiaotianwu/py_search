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
        self._manager.run() 

    def post_diskio_request(self, request):
        return self._manager.post_diskio_request(request)

    def post_stop_request(self):
        self._manager.post_stop_request()

def create_testdata(fileNum):
    os.system('mkdir testdata')
    for i in range(0, fileNum):
        fileName = 'testdata/testFile' + str(i)
        print('create ' + fileName)
        os.system('dd of=' + fileName + ' if=/dev/zero bs=1024 count=102400')

def clear_testdata():
    os.system('rm testdata -r')  

if __name__ == '__main__':
    #create_testdata(30)    

    dmThread = DiskIOManagerTestThread()
    dmThread.start()
    
    #manager = DiskIOManager()
    #gevent.spawn(manager.run)

    events = []

    for i in range(1, 31):
        req = DiskIORequest(i, 'READ', 'testdata/testfile' + str(i),
                            0, 1024 * 1024 * 10)
        ev = dmThread.post_diskio_request(req)
        #ev = manager.post_diskio_request(req)
        events.append(ev)

    for ev in events:
        ev.wait()

    print('all done')

    #manager.post_stop_request()
    dmThread.post_stop_request()

    #gevent.sleep(5)
    time.sleep(5)

    #clear_testdata()
