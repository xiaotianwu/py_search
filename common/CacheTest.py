#!/usr/bin/python

from Cache import Cache

if __name__ == '__main__':
    cache = Cache(1)
    assert cache.size() == 0
    assert cache.capacity() == 1
    cache.add(1, 'a')
    assert cache.size() == 1
    assert cache.capacity() == 1
    assert cache.find(1) == 'a'
    cache.add(2, 'b')
    assert cache.find(1) == None
    assert cache.find(2) == 'b'
    cache.add(1, 'a')
    assert cache.find(1) == 'a'
    assert cache.find(2) == None
    cache.remove(1)
    assert cache.find(1) == None
    assert cache.size() == 0
    assert cache.capacity() == 1
    cache.add(3, 'c')
    cache.clear()
    assert cache.find(3) == None
    assert cache.size() == 0

    cache = Cache(3)
    cache.add(1, 'a')
    cache.add(2, 'b') # 1->2
    assert cache.find(1) == 'a' # 2->1
    assert cache.find(2) == 'b' # 1->2
    cache.add(3, 'c') # 1->2->3
    assert cache.find(2) == 'b' # 1->3->2
    cache.add(4, 'd') # 3->2->4
    assert cache.find(1) == None
    assert cache.find(3) == 'c' # 2->4->3
    assert cache.find(4) == 'd' # 2->3->4
    cache.add(1, 'a') # 3->4->1
    assert cache.find(2) == None
    assert cache.find(1) == 'a' # 3->4->1
    cache.remove(4) # 3->1
    assert cache.find(4) == None
    cache.remove(3) # 1
    assert cache.find(3) == None
    cache.remove(1)
    assert cache.find(1) == None
    assert cache.size() == 0
    cache.add(1, 'a')
    assert cache.find(1) == 'a'
