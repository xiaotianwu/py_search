#!/usr/bin/python

import os
from SimpleIndex import *

s = SimpleIndex()
s.add('a', set())
s.add('b', set())
h = SimpleIndexHandler(s)
h.add('a', 'b')
p = h.intersect()
assert p == set([])

s.add('c', set([1, 2, 3, 4]))
s.add('d', set([2, 3, 4, 5]))
h2 = SimpleIndexHandler(s)
h2.add('c', 'd')
h2.intersect()
assert p == set([2, 3, 4])

n = 'test.index'
writer = SimpleIndexWriter()
writer.write(s, n)
reader = SimpleIndexReader()
sClone = reader.read(n)
assert s.get_indexmap() == sClone.get_indexmap()
os.remove(n)
