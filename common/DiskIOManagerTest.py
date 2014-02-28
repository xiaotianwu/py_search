#!/usr/bin/python

from DiskIOManager import *
import time
import os

if __name__ == '__main__':
    dm = DiskIOManager()
    r1 = DiskIORequest(1, 'READ', 'testdata/testfile1', 0, -1)
    r2 = DiskIORequest(2, 'READ', 'testdata/testfile2', 0, -1)
    r3 = DiskIORequest(2, 'READ', 'testdata/testfile3', 0, -1)
    r4 = DiskIORequest(2, 'READ', 'testdata/testfile4', 0, -1)
    r5 = DiskIORequest(2, 'READ', 'testdata/testfile5', 0, -1)
    dm.post_diskio_request(r1)
    dm.post_diskio_request(r2)
    dm.post_diskio_request(r3)
    dm.post_diskio_request(r4)
    dm.post_diskio_request(r5)
    dm.start()
    dm.join()
