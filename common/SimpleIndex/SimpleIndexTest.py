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
    print s.get_indexmap()
    
    s2 = SimpleIndex()
    s2.add(1, set([1, 2, 3, 4]))
    s2.add(2, set([2, 3, 4, 5]))
    h2 = SimpleIndexHandler(s2)
    h2.add(1)
    h2.add(2)
    p2 = h2.intersect()
    assert p2 == set([2, 3, 4])
    print s2.get_indexmap()
    
    n = 'test.index'
    writer = SimpleIndexWriter()
    writer.write(s2, n)
    reader = SimpleIndexReader()
    s2Clone = reader.read(n)
    assert s2.get_indexmap() == s2Clone.get_indexmap()
    assert s.get_indexmap() != s2.get_indexmap()
    os.remove(n)
