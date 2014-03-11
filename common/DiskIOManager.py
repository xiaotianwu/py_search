import logging
from threading import Event
from threading import Thread
from threading import Lock
from Queue import Queue
from multiprocessing.pool import ThreadPool as Pool

#from gevent.pool import Pool
#from gevent.queue import Queue
#from gevent.event import Event

from Cache import ThreadSafeCache
from Common import Locking
from IORequestType import IORequest
from Logger import Logger

class DiskIOManager:
    def __init__(self, diskIOThreadNum, cacheSize):
        self._ioRequestQueue = Queue()
        self._ioThreads = Pool(diskIOThreadNum)
        # TODO Need LRU Strategy Cache?
        self._fileReaders = {}
        self._fileReadersLock = Lock()
        self._requestNum = 0
        self._cacheHitNum = 0
        self._logger = Logger.Get('DiskIOManager')
        if cacheSize == 0:
            self._cache = None
        else:
            self._cache = ThreadSafeCache(cacheSize)
        
    def CacheHitRatio(self):
        return (float)(self._cacheHitNum) / self._requestNum

    def Run(self):
        self._logger.info('start manager')
        while True:
            ioRequest = self._ioRequestQueue.get()
            if ioRequest.type == 'STOP':
                self._Stop()
                break
            elif ioRequest.type == 'READ' or ioRequest.type == 'READALL':
                self._requestNum += 1
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug('get read request, id = ' +
                                       str(ioRequest.Id))
                self._ioThreads.apply_async(self._Read, (ioRequest,))
                #self._Read(ioRequest)
            elif ioRequest.type == 'WRITE':
                self._ioThreads.apply_async(self._Write)
            else:
                pass

    def PostStopRequest(self):
        request = IORequest('STOP', None, None, None)
        self._ioRequestQueue.put(request)

    def PostIORequest(self, ioRequest):
        '''return event which can be waited'''
        newEvent = Event()
        ioRequest.finishEvent = newEvent
        cachedData = None
        if self._cache != None:
            cachedData = self._cache.Fetch(ioRequest.key);
        # if data in cache, return directly
        if cachedData != None:
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('cache hit, ' +
                                   'request id =' +
                                   ioRequest.Id)
            ioRequest.result = cachedData
            self._cacheHitNum += 1
            newEvent.set()
        else:
            self._ioRequestQueue.put(ioRequest)
        return newEvent

    def _Read(self, ioRequest):
        fileName = ioRequest.fileName
        # it's a heavy lock. Fortunately, file never be closed during
        # runtime, such that we needn't create reader in most case
        with Locking(self._fileReadersLock):
            if fileName not in self._fileReaders:
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug('create reader for ' + fileName)
                reader = self._CreateReader(ioRequest)
                reader.Open(fileName)
                self._fileReaders[fileName] = reader
            reader = self._fileReaders[fileName]

        key = ioRequest.key
        data = reader.DoRequest(ioRequest)
        ioRequest.result = data
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('finished read request: ' + str(ioRequest.Id))
        ioRequest.finishEvent.set()

        if self._cache != None:
            self._cache.Add(key, data)

    def _Write(self):
        pass

    def _Stop(self):
        try:
            self._ioThreads.close()
            self._ioThreads.join()
        except Exception as exception:
            print exception

        for reader in self._fileReaders.values():
            reader.Close()  
        self._logger.info('exit manager')

    def _CreateReader(self, ioRequest):
        raise Exception('need to implement')
