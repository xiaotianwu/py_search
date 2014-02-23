#!/usr/bin/python

import os
from SimpleIndex import *

if __name__ == '__main__':
    s = SimpleIndex()
    s.add('a', set())
    s.add('b', set())
    h = SimpleIndexHandler(s)
    h.add('a')
    h.add('b')
    p = h.intersect()
    assert p == set([])
    
    s2 = SimpleIndex()
    s2.add('c', set([1, 2, 3, 4]))
    s2.add('d', set([2, 3, 4, 5]))
    h2 = SimpleIndexHandler(s2)
    h2.add('c')
    h2.add('d')
    p2 = h2.intersect()
    assert p2 == set([2, 3, 4])
    
    n = 'test.index'
    writer = SimpleIndexWriter()
    writer.write(s2, n)
    reader = SimpleIndexReader()
    s2Clone = reader.read(n)
    assert s2.get_indexmap() == s2Clone.get_indexmap()
    assert s.get_indexmap() != s2.get_indexmap()
    os.remove(n)
