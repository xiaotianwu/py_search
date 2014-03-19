#!/usr/bin/python

import random
import time

from meliae import scanner
from meliae import loader

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
    scanner.dump_all_objects('./dump')
    mem = loader.load('./dump', show_prog = True, collapse = True)   
    mem.compute_parents()
    #mem.collapse_instance_dicts()
    mem.summarize()

    #indexManager.init(testIndexFile)
    #indexSearcher = IndexSearcher(indexManager)

    #print 'start benchmark'

    #for termIdList in testSet:
    #    result = indexSearcher.search(termIdList)
    #    print result

            #termIdList.append(self.GenRandomTermIdList())
        #print 'start searching'
        #t = time.localtime()
        #t1 = t.tm_min * 60 + t.tm_sec
        #for item in termIdList:
        #    self._indexSearcher.Search(item)
        #t = time.localtime()
        #t2 = t.tm_min * 60 + t.tm_sec
        #print 'start = %d, end = %d' % (t1, t2)
