#!/usr/bin/python

from IndexManager import IndexManager

if __name__ == '__main__':
    indexManager = IndexManager(10000, 4)
    indexFiles = ['../index_chunk/testIndex']
    indexManager.init(indexFiles)
    index, retCode = indexManager.fetch(1)
    assert retCode == True
    print(str(index))
    index, retCode = indexManager.fetch(0)
    assert retCode == False
    print(str(index))
