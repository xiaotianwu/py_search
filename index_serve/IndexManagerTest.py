#!/usr/bin/python
import os
import time
import unittest

from common.Common import GenRandomIndex
from common.uncompress_index.UncompressIndex import *
from IndexManager import IndexManager

class IndexManagerTest(unittest.TestCase):
    _index = None
    _indexManager = None
    _indexFiles = None

    def CreateTestIndex(self):
        s1 = UncompressIndex()
        for i in range(0, 3):
            s1.Add(i, GenRandomIndex())
        testFile1 = 'test1.mem.index'
        writer = UncompressIndexWriter()
        writer.Write(s1, testFile1)
        print testFile1, 'created'
        s2 = UncompressIndex()
        for i in range(3, 6):
            s2.Add(i, GenRandomIndex())
        testFile2 = 'test2.disk.index'
        writer = UncompressIndexWriter()
        writer.Write(s2, testFile2)
        print testFile2, 'created'
        s3 = UncompressIndex()
        for i in range(6, 11):
            s3.Add(i, GenRandomIndex())
        testFile3 = 'test3.mem.index'
        writer = UncompressIndexWriter()
        writer.Write(s3, testFile3)
        print testFile3, 'created'
        s4 = UncompressIndex()
        for i in range(11, 20):
            s4.Add(i, GenRandomIndex())
        testFile4 = 'test4.mem.index'
        writer = UncompressIndexWriter()
        writer.Write(s4, testFile4)
        print testFile4, 'created'
        self._indexFiles = [testFile1, testFile2, testFile3, testFile4]

    def setUp(self):
        self.CreateTestIndex()
        mappingStr = '0,2:test1.mem.index:mem;3,5:test2.disk.index:disk;' +\
                     '6,10:test3.mem.index:mem;11,19:test4.disk.index:disk'
        self._indexManager = IndexManager(4, 3, '.', mappingStr)

    def tearDown(self):
        print 'test done'
        self._indexManager.Stop()
        for f in self._indexFiles:
            os.remove(f)

    def testManager(self):
        self.assertTrue(self._indexManager.IsReady())

if __name__ == '__main__':
    unittest.main()
