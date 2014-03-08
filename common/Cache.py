import threading
from Logger import Logger

class Cache:
    '''LRU strategy'''
    class Node:
        __slots__ = ['key', 'val', 'succ', 'prev']

        def __init__(self, key, val):
            self.key = key
            self.val = val
            self.succ = None
            self.prev = None

    def __init__(self, maxElemNum):
        self._chunkHead = None
        self._chunkTail = None
        self._hashTable = {}
        self._maxElemNum = maxElemNum
        self._curElemNum = 0
        self._logger = Logger.Get('LRU')

    def Clear(self):
        self._chunkHead = None
        self._chunkTail = None
        self._hashTable.clear()
        self._curElemNum = 0
       
    def Fetch(self, key):
        self._logger.debug('fetch ' + str(self._hashTable))
        if key in self._hashTable:
            self._Update(key)
            return self._hashTable[key].val
        else:
            return None

    def Add(self, key, value):
        newNode = Cache.Node(key, value)
        self._hashTable[key] = newNode
        self._logger.debug('add ' + str(self._hashTable))
        if self._curElemNum == self._maxElemNum:
            self._logger.debug('remove ' + str(self._head().key))
            self._hashTable.pop(self._head().key)
            self._Pop()
        else:
            self._curElemNum += 1
        self._Push(newNode)

    def Remove(self, key):
        nodeToDel = self._hashTable[key]
        if nodeToDel == self._chunkHead:
            self._chunkHead = self._chunkHead.succ
        if nodeToDel == self._chunkTail:
            self._chunkTail = self._chunkTail.prev
        if nodeToDel.prev != None:
            nodeToDel.prev = nodeToDel.succ
        self._hashTable.pop(key)
        self._curElemNum -= 1

    def size(self):
        return self._curElemNum

    def capacity(self):
        return self._maxElemNum

    def _Update(self, key):
        cur = self._hashTable[key]
        if cur == self._chunkTail:
            return
        if cur == self._chunkHead:
           self._chunkHead = self._chunkHead.succ
        if cur.prev != None:
            cur.prev.succ = cur.succ
        if cur.succ != None:
            cur.succ.prev = cur.prev
        cur.succ = None
        cur.prev = self._chunkTail
        self._chunkTail.succ = cur
        self._chunkTail = cur

    def _head(self):
        return self._chunkHead

    def _tail(self):
        return self._chunkTail

    def _Pop(self):
        top = self._chunkHead
        self._chunkHead = self._chunkHead.succ
        if self._chunkHead == None:
            self._chunkTail = None
        del top
        self._logger.debug('pop ' + 'chunkHead ' +\
                           'empty ' if self._chunkHead == None\
                           else str(self._chunkHead.key) +\
                           'chunkTail ' + 'empty '\
                           if self._chunkTail == None\
                           else str(self._chunkTail.key))

    def _Push(self, node):
        if self._chunkHead == None:
            self._chunkHead = node
        if self._chunkTail != None:
            self._chunkTail.succ = node
            node.prev = self._chunkTail
        self._chunkTail = node
        self._logger.debug('push ' + 'chunkHead ' +\
                           str(self._chunkHead.key) +\
                           'chunkTail ' + str(self._chunkTail.key))

class ThreadSafeCache:
    # TODO we need to test the performance
    def __init__(self, maxElemNum):
        self._cache = Cache(maxElemNum)
        self._lock = threading.RLock()

    def Fetch(self, key):
        return self._cache.Fetch(key)
  
    def Clear(self):
        self._lock.acquire()
        self._cache.Clear()
        self._locak.release()

    def Add(self, key, value):
        self._lock.acquire()
        self._cache.Add(key, value)
        self._lock.release()

    def Remove(self, key):
        self._lock.acquire()
        self._cache.Remove(key)
        self._lock.release()
