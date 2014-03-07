#!/usr/bin/python

import os
from NonCompressIndex import *

if __name__ == '__main__':
    s = NonCompressIndex()
    s.add(1, set())
    s.add(2, set())
    assert s.fetch(1) == set()
    assert s.fetch(0) == None

    h = NonCompressIndexHandler()
    h.add(s.fetch(1))
    h.add(s.fetch(2))
    p = h.intersect()
    assert p == set([])
    p = h.union()
    assert p == set([])
    
    s2 = NonCompressIndex()
    s2.add(1, set([(1, 1.0), (2, 0.9), (3, 0.8), (4, 0.7)]))
    s2.add(2, set([(2, 0.9), (3, 0.8), (4, 0.7), (5, 0.6)]))
    s2.add(3, set([(3, 0.8), (4, 0.7), (5, 0.6), (6, 0.5)]))
    h2 = NonCompressIndexHandler()
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

    testIndex = 'test.index'
    writer = NonCompressIndexWriter()
    writer.write(s2, testIndex)
    reader = NonCompressIndexReader()
    s2Clone = reader.read(testIndex)
    assert s2.get_indexmap() == s2Clone.get_indexmap()
    assert s.get_indexmap() != s2.get_indexmap()
    os.remove(testIndex)
