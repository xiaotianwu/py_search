#!/usr/bin/python

import os
import sys
sys.path.append('../common/SimpleIndex')

from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexWriter

from IndexManager import IndexManager

indexFileName = 'test.index'

def create_testdata():
    s = SimpleIndex()
    s.add(1, set([1, 2, 3]))
    s.add(2, set([2, 3, 4]))
    s.add(3, set([3, 4, 5]))
    s.add(4, set([4, 5, 6]))
    writer = SimpleIndexWriter()
    writer.write(s, indexFileName)

def delete_testdata():
    os.remove(indexFileName)

if __name__ == '__main__':
    create_testdata()

    indexManager = IndexManager()
    assert indexManager.is_ready() == False
    indexManager.init(indexFileName)
    assert indexManager.is_ready() == True

    index, retCode = indexManager.fetch(0)
    assert index == None
    assert retCode == False
    index, retCode = indexManager.fetch(1) 
    assert index == set([1, 2, 3])
    assert retCode == True
    index, retCode = indexManager.fetch(2)
    assert index == set([2, 3, 4])
    index, retCode = indexManager.fetch(3)
    assert index == set([3, 4, 5])
    index, retCode = indexManager.fetch(4)
    assert index == set([4, 5, 6])

    delete_testdata()
