#!/usr/bin/python

import os

from common.Common import GenRandomIndex
from common.uncompress_index_dealer.UncompressIndex import *
from IndexManager import IndexManager

indexFileName = 'test.index'

def CreateTestData():
    index = UncompressIndex()
    for i in range(0, 100):
        index.Add(i, GenRandomIndex())

    writer = UncompressIndexWriter()
    writer.write(index, indexFileName)

def DeleteTestData():
    os.remove(indexFileName)

if __name__ == '__main__':
    index = CreateTestData()

    indexManager = IndexManager()
    assert indexManager.IsReady() == False
    indexManager.Init(indexFileName)
    assert indexManager.IsReady() == True

    index, retCode = indexManager.Fetch(0)
    assert index == None
    assert retCode == False
    index, retCode = indexManager.Fetch(1) 
    assert index == set([1, 2, 3])
    assert retCode == True
    index, retCode = indexManager.Fetch(2)
    assert index == set([2, 3, 4])
    index, retCode = indexManager.Fetch(3)
    assert index == set([3, 4, 5])
    index, retCode = indexManager.Fetch(4)
    assert index == set([4, 5, 6])

    DeleteTestData()
