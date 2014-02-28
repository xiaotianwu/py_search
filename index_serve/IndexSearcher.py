import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from twisted.internet.defer import Deferred

import IndexServing
from SimpleIndex import *

class IndexSearcher:
    '''the worker to do the docid match'''
    def __init__(self, simpleIndex):
        if not isinstance(simpleIndex, SimpleIndex):
            raise TypeError('input must be SimpleIndex')
        self._indexHandler = SimpleIndexHandler(simpleIndex)
 
    def search(self, termIdList):
        self._indexHandler.clear()
        #d = Deferred()
        #d.addCallbacks(load_index, load_index)
        for termid in termIdList:
            self._indexHandler.add(termid)
        result = self._indexHandler.intersect()
        return self.search_callback(result)

    def search_callback(self, result):
        print(result)
        return result
