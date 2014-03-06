#!/usr/bin/python

import random
import time

from IndexManager import IndexManager
from IndexSearcher import IndexSearcher

testIndexFile = '../index_chunk/randomIndex'
termListMaxLen = 5
termIdMaxRange = 1000000

def gen_random_termidlist():
    #termListLen = random.randint(2, termListMaxLen)
    termListLen = 2
    i = 0
    termIdList = set()
    while i < termListLen:
        termId = random.randint(0, termIdMaxRange)
        if termId in termIdList:
            continue
        else:
           termIdList.add(termId)
           i += 1
    return list(termIdList)

def create_test_data():
    testSetSize = 100000
    testSet = []
    for i in range(1, testSetSize):
        testSet.append(gen_random_termidlist())
    return testSet

if __name__ == '__main__':
    #testSet = create_test_data()
    #print 'create test data finished'

    indexManager = IndexManager()
    time.sleep(100)
    #indexManager.init(testIndexFile)
    #indexSearcher = IndexSearcher(indexManager)

    #print 'start benchmark'

    #for termIdList in testSet:
    #    result = indexSearcher.search(termIdList)
    #    print result
