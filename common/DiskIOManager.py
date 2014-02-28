#import threading
import time
from Queue import Queue
from multiprocessing.pool import ThreadPool as Pool

#from gevent.pool import Pool
#from gevent.queue import Queue

from Logger import Logger

class DiskIORequest:
    def __init__(self, requestId, requestType, fileName, offset, length):
        self.Id = requestId
        self.Type = requestType
        self.fileName = fileName
        self.offset = offset
        self.length = length
        self.result = None
        self.retCode = 0 # TODO use enum to replace it

class DiskIOManager:
    def __init__(self, diskIOThreadNum = 5, maxTask = 30):
        self._ioRequestQueue = Queue()
        #self._ioThreads = Pool(processes = diskIOThreadNum)
        self._ioThreads = Pool(diskIOThreadNum)
        # TODO use LRU to cache fileDesc when opened file is more than 1024
        self._fileDescCache = {}
        self._ioCompleteSet = {}
        self._logger = Logger.get('IOThread')
        self._curTask = 0
        self._logger.debug('start manager')
        self._maxTask = 30
        
    def _stop(self):
        #self._ioThreads.close()
        self._logger.debug('exit manager')

    def run(self):
        while True:
            ioRequest = self._ioRequestQueue.get()
            if ioRequest.Type == 'STOP':
                self._stop()
                break
            elif ioRequest.Type == 'READ':
                if ioRequest.fileName not in self._fileDescCache:
                    name = ioRequest.fileName
                    self._fileDescCache[name] = open(name, 'r')
                #self._logger.debug('enter read thread')
                self._ioThreads.apply_async(self._read_from_disk, (ioRequest,))
            elif ioRequest.Type == 'WRITE':
                continue
            else:
                continue

    def _read_from_disk(self, ioRequest):
        # TODO generate debugString only when the debug mode is enable
        #debugString = 'start reading, fileName = ' + ioRequest.fileName +\
        #              ', offset = ' + str(ioRequest.offset) +\
        #              ', len = ' + str(ioRequest.length)
        #self._logger.debug(debugString)

        fd = self._fileDescCache[ioRequest.fileName]
        fd.seek(ioRequest.offset)
        if ioRequest.length == -1:
            data = fd.read()
        else:
            data = fd.read(ioRequest.length)
        #self._logger.debug('finished reading')
        self._curTask += 1
        if self._curTask == self._maxTask:
            self._logger.debug('finish all task')
            self.post_close_request()

        ioRequest.result = data
        self._ioCompleteSet[ioRequest.Id] = ioRequest

    def post_close_request(self):
        request = DiskIORequest(-1, 'STOP', '', -1, -1)
        self._ioRequestQueue.put(request)

    def post_diskio_request(self, request):
        self._ioRequestQueue.put(request)
