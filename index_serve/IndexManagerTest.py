#!/usr/bin/python
import os
import pdb
import time
import unittest

from common.Common import GenRandomIndex
from common.simple_index.SimpleIndex import *
from IndexManager import IndexManager

class IndexManagerTest(unittest.TestCase):
    def CreateTestIndex(self):
        self.s1 = SimpleIndex()
        for i in range(0, 300):
            self.s1.Add(i, GenRandomIndex())
        testFile1 = 'test1.mem.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s1, testFile1)
        print testFile1, 'created'

        self.s2 = SimpleIndex()
        for i in range(300, 600):
            self.s2.Add(i, GenRandomIndex())
        testFile2 = 'test2.disk.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s2, testFile2)
        print testFile2, 'created'

        self.s3 = SimpleIndex()
        for i in range(600, 1100):
            self.s3.Add(i, GenRandomIndex())
        testFile3 = 'test3.mem.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s3, testFile3)
        print testFile3, 'created'

        self.s4 = SimpleIndex()
        for i in range(1100, 2000):
            self.s4.Add(i, GenRandomIndex())
        testFile4 = 'test4.disk.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s4, testFile4)
        print testFile4, 'created'

        self.s5 = SimpleIndex()
        for i in range(2000, 3000):
            self.s5.Add(i, GenRandomIndex())
        testFile5 = 'test5.disk.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s5, testFile5)
        print testFile5, 'created'

        self.s6 = SimpleIndex()
        for i in range(3000, 3500):
            self.s6.Add(i, GenRandomIndex())
        testFile6 = 'test6.mem.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s6, testFile6)
        print testFile6, 'created'

        self.s7 = SimpleIndex()
        for i in range(3500, 4500):
            self.s7.Add(i, GenRandomIndex())
        testFile7 = 'test7.disk.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s7, testFile7)
        print testFile7, 'created'

        self.s8 = SimpleIndex()
        for i in range(4500, 5500):
            self.s8.Add(i, GenRandomIndex())
        testFile8 = 'test8.mem.index'
        writer = SimpleIndexWriter()
        writer.Write(self.s8, testFile8)
        print testFile8, 'created'

        self._indexFiles = [testFile1, testFile2, testFile3, testFile4,
                            testFile5, testFile6, testFile7, testFile8]

    def setUp(self):
        self.CreateTestIndex()
        mappingStr =\
            '0,299:test1.mem.index:mem;300,599:test2.disk.index:disk;' +\
            '600,1099:test3.mem.index:mem;1100,1999:test4.disk.index:disk;' +\
            '2000,2999:test5.disk.index:disk;3000,3499:test6.mem.index:mem;' +\
            '3500,4499:test7.disk.index:disk;4500,5499:test8.mem.index:mem'    
        self._indexManager = IndexManager(4, 3, '.', mappingStr)

    def tearDown(self):
        print 'test done'
        self._indexManager.Stop()
        for f in self._indexFiles:
            os.remove(f)

    def testManager(self):
        self.assertTrue(self._indexManager.IsReady())
        for i in range(0, 300):
            self.assertEqual(self._indexManager.Fetch(i)[0], self.s1.Fetch(i))
        for i in range(300, 600):
            (req, retCode) = self._indexManager.Fetch(i)
            self.assertFalse(retCode)
            req.Wait()
            self.assertEqual(req.result, self.s2.Fetch(i))
        for i in range(600, 1100):
            self.assertEqual(self._indexManager.Fetch(i)[0], self.s3.Fetch(i))
        for i in range(1100, 2000):
            (req, retCode) = self._indexManager.Fetch(i)
            self.assertFalse(retCode)
            req.Wait()
            self.assertEqual(req.result, self.s4.Fetch(i))
        for i in range(2000, 3000):
            (req, retCode) = self._indexManager.Fetch(i)
            self.assertFalse(retCode)
            req.Wait()
            self.assertEqual(req.result, self.s5.Fetch(i))
        for i in range(3000, 3500):
            self.assertEqual(self._indexManager.Fetch(i)[0], self.s6.Fetch(i))
        for i in range(3500, 4500):
            (req, retCode) = self._indexManager.Fetch(i)
            self.assertFalse(retCode)
            req.Wait()
            self.assertEqual(req.result, self.s7.Fetch(i))
        for i in range(4500, 5500):
            self.assertEqual(self._indexManager.Fetch(i)[0], self.s8.Fetch(i))
             
if __name__ == '__main__':
    unittest.main()
