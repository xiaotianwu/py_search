#!/usr/bin/python

import os
import unittest

from IndexManager import IndexManager
from IndexSearcher import IndexSearcher

indexFileName = 'test.index'

class IndexSearcherTest(unittest.TestCase):

    def CreateTestIndex(self):
        self.s1 = UncompressIndex()
        for i in range(0, 3):
            self.s1.Add(i, GenRandomIndex())
        testFile1 = 'test1.mem.index'
        writer = UncompressIndexWriter()
        writer.Write(self.s1, testFile1)
        print testFile1, 'created'
        self.s2 = UncompressIndex()
        for i in range(3, 6):
            self.s2.Add(i, GenRandomIndex())
        testFile2 = 'test2.disk.index'
        writer = UncompressIndexWriter()
        writer.Write(self.s2, testFile2)
        print testFile2, 'created'
        self.s3 = UncompressIndex()
        for i in range(6, 11):
            self.s3.Add(i, GenRandomIndex())
        testFile3 = 'test3.mem.index'
        writer = UncompressIndexWriter()
        writer.Write(self.s3, testFile3)
        print testFile3, 'created'
        self.s4 = UncompressIndex()
        for i in range(11, 20):
            self.s4.Add(i, GenRandomIndex())
        testFile4 = 'test4.disk.index'
        writer = UncompressIndexWriter()
        writer.Write(self.s4, testFile4)
        print testFile4, 'created'
        self._indexFiles = [testFile1, testFile2, testFile3, testFile4]

    def setUp(self):
        self.CreateTestIndex()
        mappingStr = '0,2:test1.mem.index:mem;3,5:test2.disk.index:disk;' +\
                     '6,10:test3.mem.index:mem;11,19:test4.disk.index:disk'
        self._indexManager = IndexManager(4, 3, '.', mappingStr)
        self._indexSearcher = IndexSearcher(indexManager)

    def tearDown(self):
        print 'test done'
        self._indexManager.Stop()
        for f in self._indexFiles:
            os.remove(f)

    def testSearcher(self):
        assert indexSearcher.search([0, 1]) == set()
        assert indexSearcher.search([1, 2]) == set([2, 3])
        assert indexSearcher.search([1, 2, 3]) == set([3])
        assert indexSearcher.search([1, 2, 3, 4]) == set()

if __name__ == '__main__':
    unittest.main()
