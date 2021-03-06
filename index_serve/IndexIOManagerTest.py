#!/usr/bin/python

import os
import random
import shutil
#import gevent
import threading
import unittest

from common.Common import GenRandomIndex
from common.simple_index.SimpleIndex import SimpleIndex
from common.simple_index.SimpleIndex import SimpleIndexWriter
from IndexIOManager import IndexIOManagerThread
from IndexIOManager import IndexIORequest

class IndexIOManagerTest(unittest.TestCase):
    _index = None

    def CreateTestData(self, begin, end):
        if os.path.exists('testdata'):
            shutil.rmtree('testdata')
        os.mkdir('testdata')
        index = SimpleIndex()
        for i in range(0, 10000):
            index.Add(i, GenRandomIndex())
    
        fileNameBase = 'testdata/testFile' + str(begin)
        print('create index file' + fileNameBase)
        writer = SimpleIndexWriter()
        writer.Write(index, fileNameBase)
    
        for i in range(begin + 1, end):
            fileName = 'testdata/testFile' + str(i)
            cp = 'cp ' + fileNameBase + ' ' + fileName
            print cp
            os.system(cp)
    
        return index

    def setUp(self):
        self._index = self.CreateTestData(0, 10)
        #manager = IndexIOManager()
        #gevent.spawn(manager.run)
        self._ioManagerThread = IndexIOManagerThread(4, 5000)
        #self._ioManagerThread = IndexIOManagerThread(4, 0)
        self._ioManagerThread.start()

    def tearDown(self):
        os.system('rm testdata -r')  

    def testRandomRead(self):
        requests = []

        for i in range(0, 5000):
            fileName = 'testdata/testFile' + str(i % 10)
            req = IndexIORequest('READ', fileName,
                                 random.randint(0, 9999))
            requests.append(req)
            self._ioManagerThread.PostIORequest(req)

        for req in requests:
            req.Wait()
            self.assertEqual(req.result, self._index.Fetch(req.key))
        
        #manager.PostStopRequest()
        self._ioManagerThread.PostStopRequest()
        self._ioManagerThread.join()

        print 'Cache Hit Ratio:', self._ioManagerThread._manager.CacheHitRatio()

if __name__ == '__main__':
    unittest.main()
