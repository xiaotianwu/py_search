#!/usr/bin/python

from DiskIOManager import *
import time
import os

if __name__ == '__main__':
    dm = DiskIOManager()
    for i in range(1, 31):
        r = DiskIORequest(i, 'READ', 'testdata/testfile' + str(i), 0, 1024 * 1024 * 10)
        dm.post_diskio_request(r)
    dm.run()
