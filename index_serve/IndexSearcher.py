import logging
from threading import Event
import uuid

from common.Logger import Logger
from IndexManager import IndexManager
from IndexConfig import IndexHandlerFactory
from multiprocessing.pool import ThreadPool as Pool

class IndexSearchRequest:
      def __init__(self, termIdList):
          self.termIdList = termIdList
          self.id = uuid.uuid4()
          self.indexHandler = IndexHandlerFactory.Get()
          self.finishEvent = Event()
          self.waitingIORequests = []
          self.result = None

      def Wait(self):
          self.finishEvent.wait()

class IndexSearcher:
    '''the worker to do docid matching'''
    def __init__(self, searchThreadNum, indexManager):
        self._indexManager = indexManager
        self._logger = Logger.get('IndexSearcher')
        self._searchThreads = Pool(searchThreadNum)

    # proc search_perpare -> searching -> search_done TODO make the proc async
    def PostSearchRequest(self, indexSearchRequest):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('SearchPrepare, termIdList = ' + str(termIdList))
        return self._SearchPrepare(indexSearchRequest)

    def _SearchPrepare(self, indexSearchRequest):
        for termId in termIdList:
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('fetch term ' + str(termId))
            (ret, retCode) = self._indexManager.Fetch(termId)
            if retCode == True:
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug('fetch term ' + str(termId) + ' success')
                indexSearchRequest.indexHandler.add(ret)
            else:
                if ret == None:
                    if self._logger.isEnabledFor(logging.DEBUG):
                        self._logger.debug('term ' + str(termId) + ' not exist')
                    return None
                else:
                    indexSearchRequest.waitingIORequests.append(ret)
        self._searchThreads.apply_async(self._Searching, (indexSearchRequest,))

    def _Searching(self, indexSearchRequest):
        waitingRequests = indexSearchRequest.waitingIORequests
        indexHandler = indexSearchRequest.indexHandler
        for req in waitingRequests:
            req.Wait()
            indexHandler.Add(req.result)
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('all posting list are ready, searching for id: ' +
                               indexSearchRequest.id)
        indexSearchRequest.result = indexHandler.Intersect()
        indexSearchRequest.finishEvent.set()
