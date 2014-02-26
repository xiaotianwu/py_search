import sys
sys.path.append('thrift/gen-py/index_serving')
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

import IndexServing
from ttypes import IndexServingStatus
from ttypes import IndexServingProperty
from SimpleIndex import *
from Common import async

# move the class to separated .py later
class IndexSearcher:
    '''the worker to do the docid match'''
    def __init__(self, simpleIndex):
        assert isinstance(simpleIndex, SimpleIndex)
        self._indexHandler = SimpleIndexHandler(simpleIndex)
 
    #@async
    def search(self, termList):
        self._indexHandler.clear()
        for term in termList:
            self._indexHandler.add(term)
        result = self._indexHandler.intersect()
        self.search_callback(result)
    
    #@async
    def search_callback(self, result):
        print result

class IndexServingHandler(IndexServing.Iface):
    '''the main handler of index serving'''
    def __init__(self, index, searcherNum = 1):
        self._indexSearcher = IndexSearcher(index)
#            [IndexSearcher(index) for i in range(1, searchNum + 1)]
        
    def ping(self):
        print "incoming ping"
        return IndexServingProperty()

    def search(self, terms):
        print 'incoming search:', str(terms)
        self._indexSearcher.search(terms)
