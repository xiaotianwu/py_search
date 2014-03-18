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
          self.waitingIORequests = []
          self.result = None

class IndexSearcher:
    '''the worker to do docid matching'''
    def __init__(self, searchThreadNum, indexManager):
        self._indexManager = indexManager
        self._logger = Logger.Get('IndexSearcher')
        self._searchThreads = Pool(searchThreadNum)

    def Search(self, termIdList):
        indexSearchRequest = IndexSearchRequest(termIdList)
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('SearchPrepare, termIdList = ' + str(termIdList))
        self._Search(indexSearchRequest)
        return indexSearchRequest.result

    def _Search(self, indexSearchRequest):
        termIdList = indexSearchRequest.termIdList
        for termId in termIdList:
            (ret, retCode) = self._indexManager.Fetch(termId)
            if retCode == True:
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug('fetch term ' + str(termId) + ' success')
                indexSearchRequest.indexHandler.Add(ret)
            else:
                if ret == None:
                    if self._logger.isEnabledFor(logging.DEBUG):
                        self._logger.debug('term ' + str(termId) + ' not exist')
                    indexSearchRequest.result = None
                    return
                else:
                    if self._logger.isEnabledFor(logging.DEBUG):
                        self._logger.debug('fetch term ' + str(termId) + ' from diskio')
                    indexSearchRequest.waitingIORequests.append(ret)
        self._searchThreads.apply(self._Searching, (indexSearchRequest,))

    def _Searching(self, indexSearchRequest):
        waitingRequests = indexSearchRequest.waitingIORequests
        indexHandler = indexSearchRequest.indexHandler
        for readRequest in waitingRequests:
            readRequest.Wait()
            indexHandler.Add(readRequest.result)
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('all posting list are ready, request id: ' +
                               str(indexSearchRequest.id))
        indexSearchRequest.result = indexHandler.Intersect()
