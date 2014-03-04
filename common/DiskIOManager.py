from threading import Event
from Queue import Queue
from multiprocessing.pool import ThreadPool as Pool

#from gevent.pool import Pool
#from gevent.queue import Queue
#from gevent.event import Event

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
    def __init__(self, diskIOThreadNum = 5, maxTask = -1):
        self._ioRequestQueue = Queue()
        self._ioThreads = Pool(diskIOThreadNum)
        # TODO Need LRU Strategy Cache?
        self._fileDescCache = {}
        self._ioCompleteSet = {}
        self._logger = Logger.get('IOThread')
        self._finishedTaskNum = 0
        self._maxTaskNum = maxTask
        
    def run(self):
        self._logger.info('start diskio manager')
        while True:
            ioRequest = self._ioRequestQueue.get()
            if ioRequest.Type == 'STOP':
                self._stop()
                break
            elif ioRequest.Type == 'READ':
                if ioRequest.fileName not in self._fileDescCache:
                    name = ioRequest.fileName
                    self._fileDescCache[name] = open(name, 'r') # TODO 'rb' mode?
                self._logger.debug('enter read thread')
                self._ioThreads.apply_async(self._read_from_disk, (ioRequest,))
            elif ioRequest.Type == 'WRITE':
                continue
            else:
                continue

    def post_stop_request(self):
        request = DiskIORequest(-1, 'STOP', '', -1, -1)
        self._ioRequestQueue.put(request)

    def post_diskio_request(self, ioRequest):
        '''return event which can be waited'''
        self._ioRequestQueue.put(ioRequest)
        self._ioCompleteSet[ioRequest.Id] = Event()
        return self._ioCompleteSet[ioRequest.Id]

    def _read_from_disk(self, ioRequest):
        # TODO concat debugString only when debug is enable
        debugString = 'start reading, fileName = ' + ioRequest.fileName +\
                      ', offset = ' + str(ioRequest.offset) +\
                      ', len = ' + str(ioRequest.length)
        self._logger.debug(debugString)

        fd = self._fileDescCache[ioRequest.fileName]
        fd.seek(ioRequest.offset)
        if ioRequest.length == -1:
            data = fd.read()
        else:
            data = fd.read(ioRequest.length)
        self._logger.debug('finished reading')

        self._finishedTaskNum += 1
        if self._finishedTaskNum == self._maxTaskNum:
            self._logger.info('finish all task')
            self.post_stop_request()

        ioRequest.result = data
        self._ioCompleteSet[ioRequest.Id].set()

    def _stop(self):
        # TODO it's necessary to stop the threadPools
        self._ioThreads.close()
        for desc in self._fileDescCache.values():
            desc.close()  
        self._logger.info('exit diskio manager')
