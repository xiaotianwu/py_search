import logging
from threading import Thread

from common.DiskIOManager import DiskIOManager
from common.IORequestType import IORequest
from common.Logger import Logger
from IndexConfig import IndexReaderFactory

class IndexIORequest(IORequest):
    def __init__(self, requestType, fileName, termId):
        IORequest.__init__(self, requestType, fileName, termId)

class IndexIOManager(DiskIOManager):
    def __init__(self, diskIOThreadNum, cacheSize):
        DiskIOManager.__init__(self, diskIOThreadNum, cacheSize)
        self._logger = Logger.Get('IndexIOManager')

    def _CreateReader(self, ioRequest):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('create reader for io request:' + ioRequest.id)
        return IndexReaderFactory.Get()

class IndexIOManagerThread(Thread):
    def __init__(self, ioThreadNum, cacheSize):
        Thread.__init__(self)
        self._manager = IndexIOManager(ioThreadNum, cacheSize)

    def run(self):
        self._manager.Run() 

    def PostIORequest(self, request):
        return self._manager.PostIORequest(request)

    def PostStopRequest(self):
        self._manager.PostStopRequest()
