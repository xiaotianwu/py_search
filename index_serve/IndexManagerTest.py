#!/usr/bin/python
import os
import pdb
import time
import unittest

from common.Common import GenRandomIndex
from common.uncompress_index.UncompressIndex import *
from IndexManager import IndexManager

class IndexManagerTest(unittest.TestCase):
    _index = None
    _indexManager = None
    _indexFiles = None
    s1 = None
    s2 = None
    s3 = None
    s4 = None

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

    def tearDown(self):
        print 'test done'
        self._indexManager.Stop()
        for f in self._indexFiles:
            os.remove(f)

    def testManager(self):
        self.assertTrue(self._indexManager.IsReady())
        for i in range(0, 3):
            self.assertEqual(self._indexManager.Fetch(i)[0], self.s1.Fetch(i))
        #pdb.set_trace()
        for i in range(3, 6):
            (req, retCode) = self._indexManager.Fetch(i)
            self.assertFalse(retCode)
            req.Wait()
            self.assertEqual(req.result, self.s2.Fetch(i))
        for i in range(6, 11):
            self.assertEqual(self._indexManager.Fetch(i)[0], self.s3.Fetch(i))
        for i in range(11, 20):
            (req, retCode) = self._indexManager.Fetch(i)
            self.assertFalse(retCode)
            req.Wait()
            self.assertEqual(req.result, self.s4.Fetch(i))
             
if __name__ == '__main__':
    unittest.main()
