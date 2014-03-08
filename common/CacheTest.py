#!/usr/bin/python

from Cache import Cache

if __name__ == '__main__':
    cache = Cache(1)
    assert cache.size() == 0
    assert cache.capacity() == 1
    cache.Add(1, 'a')
    assert cache.size() == 1
    assert cache.capacity() == 1
    assert cache.Fetch(1) == 'a'
    cache.Add(2, 'b')
    assert cache.Fetch(1) == None
    assert cache.Fetch(2) == 'b'
    cache.Add(1, 'a')
    assert cache.Fetch(1) == 'a'
    assert cache.Fetch(2) == None
    cache.Remove(1)
    assert cache.Fetch(1) == None
    assert cache.size() == 0
    assert cache.capacity() == 1
    cache.Add(3, 'c')
    cache.Clear()
    assert cache.Fetch(3) == None
    assert cache.size() == 0

    cache = Cache(3)
    cache.Add(1, 'a')
    cache.Add(2, 'b') # 1->2
    assert cache.Fetch(1) == 'a' # 2->1
    assert cache.Fetch(2) == 'b' # 1->2
    cache.Add(3, 'c') # 1->2->3
    assert cache.Fetch(2) == 'b' # 1->3->2
    cache.Add(4, 'd') # 3->2->4
    assert cache.Fetch(1) == None
    assert cache.Fetch(3) == 'c' # 2->4->3
    assert cache.Fetch(4) == 'd' # 2->3->4
    cache.Add(1, 'a') # 3->4->1
    assert cache.Fetch(2) == None
    assert cache.Fetch(1) == 'a' # 3->4->1
    cache.Remove(4) # 3->1
    assert cache.Fetch(4) == None
    cache.Remove(3) # 1
    assert cache.Fetch(3) == None
    cache.Remove(1)
    assert cache.Fetch(1) == None
    assert cache.size() == 0
    cache.Add(1, 'a')
    assert cache.Fetch(1) == 'a'

    cache = Cache(5)
    cache.Add(1, 'a')
    assert cache._head().key == 1
    assert cache._tail().key == 1
    cache.Add(2, 'b')
    assert cache._head().key == 1
    assert cache._tail().key == 2
    cache.Add(3, 'c')
    assert cache._head().key == 1
    assert cache._tail().key == 3
    cache.Add(4, 'd')
    assert cache._head().key == 1
    assert cache._tail().key == 4
    cache.Add(5, 'e') # 1->2->3->4->5
    assert cache._head().key == 1
    assert cache._tail().key == 5
    assert cache.Fetch(2) == 'b' # 1->3->4->5->2
    assert cache._head().key == 1
    assert cache._tail().key == 2
    assert cache.Fetch(1) == 'a' # 3->4->5->2->1
    assert cache._head().key == 3
    assert cache._tail().key == 1
    assert cache.Fetch(1) == 'a' # 3->4->5->2->1
    assert cache._head().key == 3
    assert cache._tail().key == 1
    cache.Remove(3) # 4->5->2->1
    assert cache._head().key == 4 
    assert cache._tail().key == 1
    cache.Remove(1) # 4->5->2
    assert cache._head().key == 4 
    assert cache._tail().key == 2
    assert cache.size() == 3
    assert cache.Fetch(5) # 4->2->5
    assert cache._head().key == 4
    assert cache._tail().key == 5
    assert cache.size() == 3
    assert cache.capacity() == 5
    cache.Remove(4) # 2->5
    assert cache._head().key == 2
    assert cache._tail().key == 5
    assert cache.Fetch(4) == None
    cache.Remove(2)  # 5
    assert cache.Fetch(2) == None
    assert cache._head().key == 5
    assert cache._tail().key == 5
    cache.Clear()
    assert cache._head() == None
    assert cache._tail() == None
