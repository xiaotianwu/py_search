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
        if not isinstance(simpleIndex, SimpleIndex):
            raise TypeError('input must be SimpleIndex')
        self._indexHandler = SimpleIndexHandler(simpleIndex)
 
    #@async
    def search(self, termIdList):
        self._indexHandler.clear()
        for termid in termIdList:
            self._indexHandler.add(termid)
        result = self._indexHandler.intersect()
        return self.search_callback(result)
    
    #@async
    def search_callback(self, result):
        print result
        return result

class IndexServingHandler(IndexServing.Iface):
    '''the main handler of index serving'''
    def __init__(self, index, searcherNum = 1):
        self._indexSearcher = IndexSearcher(index)
#            [IndexSearcher(index) for i in range(1, searchNum + 1)]
        
    def load_debug_mapping(self, termidMapping):
        self._termidMapping = termidMapping

    def ping(self):
        print "incoming ping"
        return IndexServingProperty()

    def search(self, termIds):
        print 'incoming search request:', str(termIds)
        return self._indexSearcher.search(termIds)

    def search_terms(self, terms):
        print 'incoming search_term request:', str(terms)
        termIds = [self._term_to_id(term) for term in terms]
        return self._indexSearcher.search(termIds)

    def _term_to_id(self, term):
        if self._termidMapping != None and term in self._termidMapping:
            return self._termidMapping[term]
        else:
            return -1
