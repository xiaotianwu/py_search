#!/usr/bin/python

import os
import random

from UncompressIndex import *
from common.Common import GenRandomIndex

if __name__ == '__main__':
    s = UncompressIndex()
    s.Add(1, set())
    s.Add(2, set())
    assert s.Fetch(1) == set()
    assert s.Fetch(0) == None

    h = UncompressIndexHandler()
    h.Add(s.Fetch(1))
    h.Add(s.Fetch(2))
    p = h.Intersect()
    assert p == set([])
    p = h.Union()
    assert p == set([])
    
    s2 = UncompressIndex()
    s2.Add(1, set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7)]))
    s2.Add(2, set([(2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)]))
    s2.Add(3, set([(3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]))
    h2 = UncompressIndexHandler()
    h2.Add(s2.Fetch(1))
    h2.Add(s2.Fetch(2))
    p2 = h2.Intersect()
    assert p2 == set([(2, 0.9), (3, 0.8), (4, 0.7)])
    p2 = h2.Union()
    assert p2 == set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)])
    h2.Clear()
    assert h2._indexContainer == []
    h2.Add(s2.Fetch(1))
    h2.Add(s2.Fetch(2))
    h2.Add(s2.Fetch(3))
    p3 = h2.Intersect()
    assert p3 == set([(3, 0.8), (4, 0.7)])
    p3 = h2.Union()
    assert p3 == set([(1, 1.0), (2, 0.9), (3, 0.8),
                      (4, 0.7), (5, 0.6), (6, 0.5)])

    testIndex = 'tiny.index'
    writer = UncompressIndexWriter()
    writer.Write(s2, testIndex)
    reader = UncompressIndexReader()
    reader.Open(testIndex)
    s2Clone = reader.ReadAll()
    assert s2.GetIndexMap() == s2Clone.GetIndexMap()
    assert s.GetIndexMap() != s2.GetIndexMap()
    assert reader.Read(1) == set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7)])
    assert reader.Read(2) == set([(2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)])
    assert reader.Read(3) == set([(3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)])
    reader.Close()
    os.remove(testIndex)

    s3 = UncompressIndex()
    for i in range(0, 1000):
        s3.Add(i, GenRandomIndex())
    testIndex = 'large.index'
    writer.Write(s3, testIndex)

    reader = UncompressIndexReader()
    reader.Open(testIndex)
    s3Clone = reader.ReadAll()
    assert s3.GetIndexMap() == s3Clone.GetIndexMap()
    reader.Close()
    reader.Open(testIndex)
    for i in range(0, 1000):
        assert reader.Read(i) == s3.Fetch(i)
    reader.Close()

    reader = UncompressIndexReader(isMMap = True)
    reader.Open(testIndex)
    s3Clone = reader.ReadAll()
    assert s3.GetIndexMap() == s3Clone.GetIndexMap()
    reader.Close()
    reader.Open(testIndex)
    for i in range(0, 1000):
        assert reader.Read(i) == s3.Fetch(i)
    reader.Close()

    os.remove(testIndex)
