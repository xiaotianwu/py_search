#!/usr/bin/python

import os
from SimpleIndex import *

if __name__ == '__main__':
    s = SimpleIndex()
    s.add(1, set())
    s.add(2, set())
    h = SimpleIndexHandler(s)
    h.add(1)
    h.add(2)
    p = h.intersect()
    assert p == set([])
    p = h.union()
    assert p == set([])
    
    s2 = SimpleIndex()
    s2.add(1, set([1, 2, 3, 4]))
    s2.add(2, set([2, 3, 4, 5]))
    s2.add(3, set([3, 4, 5, 6]))
    h2 = SimpleIndexHandler(s2)
    h2.add(1)
    h2.add(2)
    p2 = h2.intersect()
    assert p2 == set([2, 3, 4])
    p2 = h2.union()
    assert p2 == set([1, 2, 3, 4, 5])
    h2.clear()
    assert h2._termIds == []
    h2.add(1)
    h2.add(2)
    h2.add(3)
    p3 = h2.intersect()
    assert p3 == set([3, 4])
    p3 = h2.union()
    assert p3 == set([1, 2, 3, 4, 5, 6])

    testIndex = 'test.index'
    writer = SimpleIndexWriter()
    writer.write(s2, testIndex)
    reader = SimpleIndexReader()
    s2Clone = reader.read(testIndex)
    assert s2.get_indexmap() == s2Clone.get_indexmap()
    assert s.get_indexmap() != s2.get_indexmap()
    os.remove(testIndex)
