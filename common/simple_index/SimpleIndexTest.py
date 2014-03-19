#!/usr/bin/python

import os
import random
import unittest

from SimpleIndex import *
from common.Common import GenRandomIndex

class SimpleIndexTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSimpleIndex(self):
        s = SimpleIndex()
        s.Add(1, set())
        s.Add(2, set())
        self.assertSetEqual(s.Fetch(1), set()) 
        self.assertEqual(s.Fetch(0), None) 

    def testSimpleIndexHandler1(self):
        s = SimpleIndex()
        s.Add(1, set())
        s.Add(2, set())
        self.assertSetEqual(s.Fetch(1), set()) 
        self.assertEqual(s.Fetch(0), None) 
        h = SimpleIndexHandler()
        h.Add(s.Fetch(1))
        h.Add(s.Fetch(2))
        p = h.Intersect()
        self.assertSetEqual(p, set([])) 
        p = h.Union()
        self.assertSetEqual(p, set([])) 

    def testSimpleIndexHandler2(self):
        s2 = SimpleIndex()
        s2.Add(1, set([1, 2, 3, 4]))
        s2.Add(2, set([2, 3, 4, 5]))
        s2.Add(3, set([3, 4, 5, 6]))
        h2 = SimpleIndexHandler()
        h2.Add(s2.Fetch(1))
        h2.Add(s2.Fetch(2))
        p2 = h2.Intersect()
        self.assertSetEqual(p2, set([2, 3, 4])) 
        p2 = h2.Union()
        self.assertSetEqual(p2, set([1, 2, 3, 4, 5])) 
        h2.Clear()
        self.assertEqual(h2._indexContainer, []) 
        h2.Add(s2.Fetch(1))
        h2.Add(s2.Fetch(2))
        h2.Add(s2.Fetch(3))
        p3 = h2.Intersect()
        self.assertSetEqual(p3, set([3, 4])) 
        p3 = h2.Union()
        self.assertSetEqual(p3, set([1, 2, 3, 4, 5, 6]))

    def testReadWriteWithTinySize(self):
        s2 = SimpleIndex()
        s2.Add(1, set([1, 2, 3, 4]))
        s2.Add(2, set([2, 3, 4, 5]))
        s2.Add(3, set([3, 4, 5, 6]))
        h2 = SimpleIndexHandler()
        h2.Add(s2.Fetch(1))
        h2.Add(s2.Fetch(2))
        p2 = h2.Intersect()
        self.assertSetEqual(p2, set([2, 3, 4]))
        p2 = h2.Union()
        self.assertSetEqual(p2, set([1, 2, 3, 4, 5]))
        h2.Clear()
        self.assertEqual(h2._indexContainer, []) 
        h2.Add(s2.Fetch(1))
        h2.Add(s2.Fetch(2))
        h2.Add(s2.Fetch(3))
        p3 = h2.Intersect()
        self.assertSetEqual(p3, set([3, 4])) 
        p3 = h2.Union()
        self.assertSetEqual(p3, set([1, 2, 3, 4, 5, 6]))
        testIndex = 'tiny.index'
        writer = SimpleIndexWriter()
        writer.Write(s2, testIndex)
        reader = SimpleIndexReader()
        reader.Open(testIndex)
        s2Clone = reader.ReadAll()
        self.assertEqual(s2.GetIndexMap(), s2Clone.GetIndexMap()) 
        self.assertSetEqual(reader.Read(1), set([1, 2, 3, 4]))
        self.assertSetEqual(reader.Read(2), set([2, 3, 4, 5]))
        self.assertSetEqual(reader.Read(3), set([3, 4, 5, 6]))
        reader.Close()
        os.remove(testIndex)

    def testReadWriteWithLargeSize(self):
        s3 = SimpleIndex()
        for i in range(0, 1000):
            s3.Add(i, GenRandomIndex())
        testIndex = 'large.index'
        writer = SimpleIndexWriter()
        writer.Write(s3, testIndex)

        reader = SimpleIndexReader()
        reader.Open(testIndex)
        s3Clone = reader.ReadAll()
        self.assertDictEqual(s3.GetIndexMap(), s3Clone.GetIndexMap()) 
        reader.Close()
        reader.Open(testIndex)
        for i in range(0, 1000):
            self.assertSetEqual(reader.Read(i), s3.Fetch(i)) 
        reader.Close()

        reader = SimpleIndexReader(isMMap = True)
        reader.Open(testIndex)
        s3Clone = reader.ReadAll()
        self.assertDictEqual(s3.GetIndexMap(), s3Clone.GetIndexMap()) 
        reader.Close()
        reader.Open(testIndex)
        for i in range(0, 1000):
            self.assertSetEqual(reader.Read(i), s3.Fetch(i)) 
        reader.Close()

        os.remove(testIndex)

    def testMerger(self):
        s1 = SimpleIndex()
        s1.Add(1, set([5]))
        s1.Add(2, set())
        s = SimpleIndex()
        s.Add(1, set([5]))
        s.Add(2, set())
        
        merger = SimpleIndexMerger()
        merger.Add(s1)
        mergedIndex = merger.DoMerge()
        self.assertDictEqual(mergedIndex.GetIndexMap(), s.GetIndexMap())

        s1 = SimpleIndex()
        s1.Add(1, set([5]))
        s1.Add(2, set())
        s2 = SimpleIndex()
        s2.Add(1, set([1, 2, 3, 4]))
        s2.Add(2, set([2, 3, 4, 5]))
        s2.Add(3, set([3, 4, 5, 6]))
        s3 = SimpleIndex()
        s3.Add(4, set([4, 7, 8, 10]))
        s = SimpleIndex()
        s.Add(1, set([1, 2, 3, 4, 5]))
        s.Add(2, set([2, 3, 4, 5]))
        s.Add(3, set([3, 4, 5, 6]))
        s.Add(4, set([4, 7, 8, 10]))

        merger = SimpleIndexMerger()
        merger.Add(s1)
        merger.Add(s2)
        merger.Add(s3)
        mergedIndex = merger.DoMerge()
        self.assertDictEqual(mergedIndex.GetIndexMap(), s.GetIndexMap())

if __name__ == '__main__':
    unittest.main()
