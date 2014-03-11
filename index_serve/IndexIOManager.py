from threading import Thread

from common.DiskIOManager import DiskIOManager
from common.uncompress_index.UncompressIndex import UncompressIndexReader
from common.Logger import Logger

class IndexIOManager(DiskIOManager):
    def __init__(self, diskIOThreadNum, cacheSize):
        DiskIOManager.__init__(self, diskIOThreadNum, cacheSize)
        self._logger = Logger.Get('IndexIOManager')

    def _CreateReader(self, ioRequest):
        # ugly polymorphic
        if ioRequest.fileType == 'UncompressIndex':
            # close mmap in 32bit system
            return UncompressIndexReader(isMMap = False)
        else:
            raise Exception('unknown io request type ' + ioRequest.fileType)

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
