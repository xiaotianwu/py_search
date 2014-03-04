#!/usr/bin/python

from Cache import Cache

if __name__ == '__main__':
    cache = Cache(1)
    assert cache.size() == 0
    assert cache.capacity() == 1
    cache.add(1, 'a')
    assert cache.size() == 1
    assert cache.capacity() == 1
    assert cache.fetch(1) == 'a'
    cache.add(2, 'b')
    assert cache.fetch(1) == None
    assert cache.fetch(2) == 'b'
    cache.add(1, 'a')
    assert cache.fetch(1) == 'a'
    assert cache.fetch(2) == None
    cache.remove(1)
    assert cache.fetch(1) == None
    assert cache.size() == 0
    assert cache.capacity() == 1
    cache.add(3, 'c')
    cache.clear()
    assert cache.fetch(3) == None
    assert cache.size() == 0

    cache = Cache(3)
    cache.add(1, 'a')
    cache.add(2, 'b') # 1->2
    assert cache.fetch(1) == 'a' # 2->1
    assert cache.fetch(2) == 'b' # 1->2
    cache.add(3, 'c') # 1->2->3
    assert cache.fetch(2) == 'b' # 1->3->2
    cache.add(4, 'd') # 3->2->4
    assert cache.fetch(1) == None
    assert cache.fetch(3) == 'c' # 2->4->3
    assert cache.fetch(4) == 'd' # 2->3->4
    cache.add(1, 'a') # 3->4->1
    assert cache.fetch(2) == None
    assert cache.fetch(1) == 'a' # 3->4->1
    cache.remove(4) # 3->1
    assert cache.fetch(4) == None
    cache.remove(3) # 1
    assert cache.fetch(3) == None
    cache.remove(1)
    assert cache.fetch(1) == None
    assert cache.size() == 0
    cache.add(1, 'a')
    assert cache.fetch(1) == 'a'

    cache = Cache(5)
    cache.add(1, 'a')
    assert cache._head().key == 1
    assert cache._tail().key == 1
    cache.add(2, 'b')
    assert cache._head().key == 1
    assert cache._tail().key == 2
    cache.add(3, 'c')
    assert cache._head().key == 1
    assert cache._tail().key == 3
    cache.add(4, 'd')
    assert cache._head().key == 1
    assert cache._tail().key == 4
    cache.add(5, 'e') # 1->2->3->4->5
    assert cache._head().key == 1
    assert cache._tail().key == 5
    assert cache.fetch(2) == 'b' # 1->3->4->5->2
    assert cache._head().key == 1
    assert cache._tail().key == 2
    assert cache.fetch(1) == 'a' # 3->4->5->2->1
    assert cache._head().key == 3
    assert cache._tail().key == 1
    assert cache.fetch(1) == 'a' # 3->4->5->2->1
    assert cache._head().key == 3
    assert cache._tail().key == 1
    cache.remove(3) # 4->5->2->1
    assert cache._head().key == 4 
    assert cache._tail().key == 1
    cache.remove(1) # 4->5->2
    assert cache._head().key == 4 
    assert cache._tail().key == 2
    assert cache.size() == 3
    assert cache.fetch(5) # 4->2->5
    assert cache._head().key == 4
    assert cache._tail().key == 5
    assert cache.size() == 3
    assert cache.capacity() == 5
    cache.remove(4) # 2->5
    assert cache._head().key == 2
    assert cache._tail().key == 5
    assert cache.fetch(4) == None
    cache.remove(2)  # 5
    assert cache.fetch(2) == None
    assert cache._head().key == 5
    assert cache._tail().key == 5
    cache.clear()
    assert cache._head() == None
    assert cache._tail() == None
