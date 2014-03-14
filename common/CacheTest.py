#!/usr/bin/python

import unittest

from Cache import Cache

class CacheTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCase1(self):
        cache = Cache(1)
        self.assertEqual(cache.size(), 0) 
        self.assertEqual(cache.capacity(), 1) 
        cache.Add(1, 'a')
        self.assertEqual(cache.size(), 1) 
        self.assertEqual(cache.capacity(), 1) 
        self.assertEqual(cache.Fetch(1), 'a') 
        cache.Add(2, 'b')
        self.assertEqual(cache.Fetch(1), None) 
        self.assertEqual(cache.Fetch(2), 'b') 
        cache.Add(1, 'a')
        self.assertEqual(cache.Fetch(1), 'a') 
        self.assertEqual(cache.Fetch(2), None) 
        cache.Remove(1)
        self.assertEqual(cache.Fetch(1), None) 
        self.assertEqual(cache.size(), 0) 
        self.assertEqual(cache.capacity(), 1) 
        cache.Add(3, 'c')
        cache.Clear()
        self.assertEqual(cache.Fetch(3), None) 
        self.assertEqual(cache.size(), 0) 

    def testCase2(self):
        cache = Cache(3)
        cache.Add(1, 'a')
        cache.Add(2, 'b') # 1->2
        self.assertEqual(cache.Fetch(1), 'a') # 2->1
        self.assertEqual(cache.Fetch(2), 'b') # 1->2
        cache.Add(3, 'c') # 1->2->3
        self.assertEqual(cache.Fetch(2), 'b') # 1->3->2
        cache.Add(4, 'd') # 3->2->4
        self.assertEqual(cache.Fetch(1), None) 
        self.assertEqual(cache.Fetch(3), 'c') # 2->4->3
        self.assertEqual(cache.Fetch(4), 'd') # 2->3->4
        cache.Add(1, 'a') # 3->4->1
        self.assertEqual(cache.Fetch(2), None) 
        self.assertEqual(cache.Fetch(1), 'a') # 3->4->1
        cache.Remove(4) # 3->1
        self.assertEqual(cache.Fetch(4), None) 
        cache.Remove(3) # 1
        self.assertEqual(cache.Fetch(3), None) 
        cache.Remove(1)
        self.assertEqual(cache.Fetch(1), None) 
        self.assertEqual(cache.size(), 0) 
        cache.Add(1, 'a')
        self.assertEqual(cache.Fetch(1), 'a') 

    def testCase3(self):
        cache = Cache(5)
        cache.Add(1, 'a')
        self.assertEqual(cache._head().key, 1) 
        self.assertEqual(cache._tail().key, 1) 
        cache.Add(2, 'b')
        self.assertEqual(cache._head().key, 1) 
        self.assertEqual(cache._tail().key, 2) 
        cache.Add(3, 'c')
        self.assertEqual(cache._head().key, 1) 
        self.assertEqual(cache._tail().key, 3) 
        cache.Add(4, 'd')
        self.assertEqual(cache._head().key, 1) 
        self.assertEqual(cache._tail().key, 4) 
        cache.Add(5, 'e') # 1->2->3->4->5
        self.assertEqual(cache._head().key, 1) 
        self.assertEqual(cache._tail().key, 5) 
        self.assertEqual(cache.Fetch(2), 'b') # 1->3->4->5->2
        self.assertEqual(cache._head().key, 1) 
        self.assertEqual(cache._tail().key, 2) 
        self.assertEqual(cache.Fetch(1), 'a') # 3->4->5->2->1
        self.assertEqual(cache._head().key, 3) 
        self.assertEqual(cache._tail().key, 1) 
        self.assertEqual(cache.Fetch(1), 'a') # 3->4->5->2->1
        self.assertEqual(cache._head().key, 3) 
        self.assertEqual(cache._tail().key, 1) 
        cache.Remove(3) # 4->5->2->1
        self.assertEqual(cache._head().key, 4) 
        self.assertEqual(cache._tail().key, 1) 
        cache.Remove(1) # 4->5->2
        self.assertEqual(cache._head().key, 4) 
        self.assertEqual(cache._tail().key, 2) 
        self.assertEqual(cache.size(), 3) 
        assert cache.Fetch(5) # 4->2->5
        self.assertEqual(cache._head().key, 4) 
        self.assertEqual(cache._tail().key, 5) 
        self.assertEqual(cache.size(), 3) 
        self.assertEqual(cache.capacity(), 5) 
        cache.Remove(4) # 2->5
        self.assertEqual(cache._head().key, 2) 
        self.assertEqual(cache._tail().key, 5) 
        self.assertEqual(cache.Fetch(4), None) 
        cache.Remove(2)  # 5
        self.assertEqual(cache.Fetch(2), None) 
        self.assertEqual(cache._head().key, 5) 
        self.assertEqual(cache._tail().key, 5) 
        cache.Clear()
        self.assertEqual(cache._head(), None) 
        self.assertEqual(cache._tail(), None) 

if __name__ == '__main__':
    unittest.main()
