#!/usr/bin/python
import os
import time
import unittest

from common.Common import GenRandomIndex
from common.uncompress_index.UncompressIndex import *
from IndexManager import IndexManager

class IndexManagerTest(unittest.TestCase):
    self._index = None
    self._indexManager = None
    self._indexFile = 'test.index'

    def setUp(self):
        index = UncompressIndex()
        for i in range(0, 1000):
            index.Add(i, GenRandomIndex())
        self._index = index
        writer = UncompressIndexWriter()
        writer.Write(self._index, self._indexFile)
        print self._indexFile, 'created'
        self._indexManager = IndexManager(0, 3)
        self._indexManager.Init(self._indexFile)

    def tearDown(self):
        print 'test done'
        self._indexManager.Stop()
        os.remove(self._indexFile)

    def testManager(self):
        self.assertTrue(assert self._indexManager.IsReady())

        for i in range(0, 1000):
            print 'test case', i
            assert self._index.Fetch(i) == self._indexManager.Fetch(i)[0]

if __name__ == '__main__':
    unittest.main()
