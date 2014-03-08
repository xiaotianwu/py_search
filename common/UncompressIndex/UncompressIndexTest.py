#!/usr/bin/python

import os
import random

from UncompressIndex import *

randomIndexLen = 1000

def gen_random_index():
    i = 0
    s = set()
    while i < randomIndexLen:
        (item1, item2) = (random.randint(0, 10000),
                          random.randint(0, 10000))
        if (item1, item2) in s:
            continue
        else:
            s.add((item1, item2))
            i += 1
    return s

if __name__ == '__main__':
    s = UncompressIndex()
    s.add(1, set())
    s.add(2, set())
    assert s.fetch(1) == set()
    assert s.fetch(0) == None

    h = UncompressIndexHandler()
    h.add(s.fetch(1))
    h.add(s.fetch(2))
    p = h.intersect()
    assert p == set([])
    p = h.union()
    assert p == set([])
    
    s2 = UncompressIndex()
    s2.add(1, set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7)]))
    s2.add(2, set([(2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)]))
    s2.add(3, set([(3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]))
    h2 = UncompressIndexHandler()
    h2.add(s2.fetch(1))
    h2.add(s2.fetch(2))
    p2 = h2.intersect()
    assert p2 == set([(2, 0.9), (3, 0.8), (4, 0.7)])
    p2 = h2.union()
    assert p2 == set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)])
    h2.clear()
    assert h2._indexContainer == []
    h2.add(s2.fetch(1))
    h2.add(s2.fetch(2))
    h2.add(s2.fetch(3))
    p3 = h2.intersect()
    assert p3 == set([(3, 0.8), (4, 0.7)])
    p3 = h2.union()
    assert p3 == set([(1, 1.0), (2, 0.9), (3, 0.8),
                      (4, 0.7), (5, 0.6), (6, 0.5)])

    testIndex = 'tiny.index'
    writer = UncompressIndexWriter()
    writer.write(s2, testIndex)
    reader = UncompressIndexReader()
    reader.load(testIndex)
    s2Clone = reader.read_all()
    assert s2.get_indexmap() == s2Clone.get_indexmap()
    assert s.get_indexmap() != s2.get_indexmap()
    assert reader.read(1) == set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7)])
    assert reader.read(2) == set([(2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)])
    assert reader.read(3) == set([(3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)])
    reader.unload()
    os.remove(testIndex)

    s3 = UncompressIndex()
    for i in range(0, 1000):
        s3.add(i, gen_random_index())
    testIndex = 'large.index'
    writer.write(s3, testIndex)
    reader = UncompressIndexReader()
    reader.load(testIndex)
    s3Clone = reader.read_all()
    assert s3.get_indexmap() == s3Clone.get_indexmap()
    reader.unload()

    reader.load(testIndex)
    for i in range(0, 1000):
        assert reader.read(i) == s3.fetch(i)
    reader.unload()

    os.remove(testIndex)
