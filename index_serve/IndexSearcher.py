import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from SimpleIndex import *
from Logger import Logger

class IndexSearcher:
    '''the worker to do docid matching'''
    def __init__(self, indexManager):
        self._indexManager = indexManager
        self._logger = Logger.get('IndexSearcher')

    # proc search_perpare -> searching -> search_done TODO make the proc async
    def search(self, termIdList):
        self._logger.debug('search_prepare, termIdList = ' + str(termIdList))
        return self.search_prepare(termIdList)

    def search_prepare(self, termIdList):
        indexHandler = SimpleIndexHandler() # TODO set a commonHandler
        for termId in termIdList:
            # TODO make fetch async
            self._logger.debug('fetch term ' + str(termId))
            index, retCode = self._indexManager.fetch(termId)
            if retCode == True:
                self._logger.debug('fetch term ' + str(termId) + ' success')
                indexHandler.add(index)
            else:
                self._logger.debug('fetch term ' + str(termId) + ' failed')
                return self.search_done(set())

        return self.searching(indexHandler)

    def searching(self, indexHandler):
        # TODO add unique trailer id
        self._logger.debug('searching')
        result = indexHandler.intersect()
        return self.search_done(result)

    def search_done(self, result):
        # TODO add unique trailer id
        self._logger.debug('search done')
        return result
