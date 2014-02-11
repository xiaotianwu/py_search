from SimpleInvertedIndex import *

# TestCase1
p1 = []
s1 = SimpleInvertedIndex('a', p1)

p2 = []
s2 = SimpleInvertedIndex('b', p2)

h = SimpleInvertedIndexHandler()
p3 = h.intersect(s1, s2)

assert p3 == []

# TestCase2
p1 = [1, 2, 3, 4]
s1 = SimpleInvertedIndex('a', p1)

p2 = [2, 3, 4, 5]
s2 = SimpleInvertedIndex('b', p2)

h = SimpleInvertedIndexHandler()
p3 = h.intersect(s1, s2)

assert p3 == [2, 3, 4]
