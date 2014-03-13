from threading import Event
from threading import Thread
from threading import Lock
from threading import RLock
from Queue import Queue
from multiprocessing.pool import ThreadPool as Pool

#from gevent.pool import Pool
#from gevent.queue import Queue
#from gevent.event import Event

from Common import Locking
from IORequestType import IORequest
from Logger import Logger
from uncompress_index.UncompressIndex import UncompressIndexIORequest
from uncompress_index.UncompressIndex import UncompressIndexReader
from plain_file.PlainFile import PlainFileIORequest
from plain_file.PlainFile import PlainFileReader

class DiskIOManager:
    def __init__(self, diskIOThreadNum, maxTaskNum):
        self._ioRequestQueue = Queue()
        self._ioThreads = Pool(diskIOThreadNum)
        # TODO Need LRU Strategy Cache?
        self._fileReaders = {}
        self._fileReadersLock = RLock()
        self._logger = Logger.Get('DiskIOManager')
        self._finishedTaskNum = 0
        self._maxTaskNum = maxTaskNum
        
    def Run(self):
        self._logger.info('start diskio manager')
        while True:
            ioRequest = self._ioRequestQueue.get()
            if ioRequest.type == 'STOP':
                self._Stop()
                break
            elif ioRequest.type == 'READ' or ioRequest.type == 'READALL':
                self._logger.debug('get read request, id = ' +
                                   str(ioRequest.Id))
                self._ioThreads.apply_async(self._Read, (ioRequest,))
                #self._Read(ioRequest)
            elif ioRequest.type == 'WRITE':
                self._ioThreads.apply_async(self._Write)
            else:
                pass

    def PostStopRequest(self):
        request = IORequest('STOP', None)
        self._ioRequestQueue.put(request)

    def PostIORequest(self, ioRequest):
        '''return event which can be waited'''
        newEvent = Event()
        ioRequest.finishEvent = newEvent
        self._ioRequestQueue.put(ioRequest)
        return newEvent

    def _Read(self, ioRequest):
        fileName = ioRequest.fileName

        # it's a heavy lock. Fortunately, file never be closed during
        # runtime, such that we needn't create reader in most case
        with Locking(self._fileReadersLock):
            if fileName not in self._fileReaders:
                self._logger.debug('create reader for ' + fileName)
                reader = self._CreateReader(ioRequest)
                reader.Open(fileName)
                self._fileReaders[fileName] = reader
            reader = self._fileReaders[fileName]

        ioRequest.result = reader.DoRequest(ioRequest)
        self._logger.debug('finished read request: ' + str(ioRequest.Id))
        ioRequest.finishEvent.set()

        self._finishedTaskNum += 1
        if self._finishedTaskNum == self._maxTaskNum:
            self._logger.info('all task finished, post stop request')
            self.PostStopRequest()

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
        self._logger.info('exit diskio manager')

    def _CreateReader(self, ioRequest):
        # ugly polymorphic
        if isinstance(ioRequest, PlainFileIORequest) == True:
            return PlainFileReader()
        elif isinstance(ioRequest, UncompressIndexIORequest) == True:
            return UncompressIndexReader()
        else:
            raise Exception('unknown io request type ' + str(ioRequest))

class DiskIOManagerThread(Thread):
    def __init__(self, ioThreadNum, maxTaskNum = -1):
        Thread.__init__(self)
        self._manager = DiskIOManager(ioThreadNum, maxTaskNum)

    def run(self):
        self._manager.Run() 

    def PostIORequest(self, request):
        return self._manager.PostIORequest(request)

    def PostStopRequest(self):
        self._manager.PostStopRequest()
