import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

import IndexServing
from SimpleIndex import *

class IndexSearcher:
    '''the worker to do docid matching'''
    def __init__(self, indexManager):
        self._indexManager = indexManager

    # proc search_perpare -> searching -> search_done TODO make the proc async
    def search(self, termIdList):
        return search_prepare(termIdList)

    def search_prepare(self, termIdList):
        indexHandler = SimpleIndexHandler() # TODO set a commonHandler
        for termId in termIdList:
            index, retCode = self._indexManager.fetch(termId) # TODO make fetch async
            if retCode == True:
                indexHandler.add(index)
        return self.searching(indexHandler)

    def searching(self, indexHandler):
        result = indexHandler.intersect()
        return self.search_done(result)

    def search_done(self, result):
        return result
