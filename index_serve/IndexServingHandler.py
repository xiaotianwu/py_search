import sys
sys.path.append('thrift/gen-py/index_serving')
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

import IndexServing
from ttypes import IndexServingStatus
from ttypes import IndexServingProperty
from SimpleIndex import *
from Common import async_process_call

class IndexSearcher:
    def __init__(self, simpleIndex):
        assert isinstance(simpleIndex, SimpleIndex)
        self._indexHandler = SimpleIndexHandler(simpleIndex)
 
    @async_process_call
    def search(self, termList):
        self._indexHandler.clear()
        for term in termList:
            self._indexHandler.add(term)
        return self._indexHandler.intersect()

class IndexServingHandler(IndexServing.Iface):
    def __init__(self, simpleIndex):
        assert isinstance(simpleIndex, SimpleIndex)
        self._indexSeacher = IndexSearcher(simpleIndex)
        
    def ping(self):
        print "incoming ping"
        return IndexServingProperty()

    def search(self, terms):
        self._indexSearcher.search(terms)
