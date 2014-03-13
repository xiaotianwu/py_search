#!/usr/bin/python

import os
import time

from common.Common import GenRandomIndex
from common.uncompress_index.UncompressIndex import *
from IndexManager import IndexManager

indexFileName = 'test.index'

def CreateTestData():
    index = UncompressIndex()
    for i in range(0, 1000):
        index.Add(i, GenRandomIndex())

    writer = UncompressIndexWriter()
    writer.Write(index, indexFileName)
    print indexFileName, 'created'
    return index

def DeleteTestData():
    os.remove(indexFileName)

if __name__ == '__main__':
    index = CreateTestData()

    indexManager = IndexManager(0, 3)
    assert indexManager.IsReady() == False
    indexManager.Init(indexFileName)
    assert indexManager.IsReady() == True

    for i in range(0, 1000):
        print 'test case', i
        assert index.Fetch(i) == indexManager.Fetch(i)[0]

    indexManager.Stop()
    print 'test done'
    DeleteTestData()
