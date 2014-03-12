from threading import Event
from threading import Thread
from threading import RLock
from Queue import Queue
from multiprocessing.pool import ThreadPool as Pool

#from gevent.pool import Pool
#from gevent.queue import Queue
#from gevent.event import Event

from Common import Locking
from IORequestType import IORequest
from Logger import Logger
from uncompress_index_dealer.UncompressIndex import UncompressIndexIORequest
from uncompress_index_dealer.UncompressIndex import UncompressIndexReader
from plain_file_dealer.PlainFile import PlainFileIORequest
from plain_file_dealer.PlainFile import PlainFileReader

class DiskIOManager:
    def __init__(self, diskIOThreadNum, maxTaskNum):
        self._ioRequestQueue = Queue()
        self._ioThreads = Pool(diskIOThreadNum)
        # TODO Need LRU Strategy Cache?
        self._fileReaders = {}
        self._fileReadersLock = RLock()
        self._ioCompleteSet = {}
        self._ioCompleteSetLock = RLock()
        self._logger = Logger.Get('DiskIOManager')
        self._finishedTaskNum = 0
        self._maxTaskNum = maxTaskNum
        
    def Run(self):
        self._logger.info('start diskio manager')
        while True:
            ioRequest = self._ioRequestQueue.get()
            if ioRequest.Type == 'STOP':
                self._Stop()
                break
            elif ioRequest.Type == 'READ' or ioRequest.Type == 'READALL':
                self._logger.debug('get read request, id = ' +
                                   str(ioRequest.Id))
                self._ioThreads.apply_async(self._Read, (ioRequest,))
                #self._Read(ioRequest)
            elif ioRequest.Type == 'WRITE':
                self._ioThreads.apply_async(self._Write)
            else:
                pass

    def PostStopRequest(self):
        request = IORequest(-1, 'STOP', None)
        self._ioRequestQueue.put(request)

    def PostIORequest(self, ioRequest):
        '''return event which can be waited'''
        assert ioRequest.Id not in self._ioCompleteSet
        self._ioCompleteSet[ioRequest.Id] = Event()
        self._ioRequestQueue.put(ioRequest)
        return self._ioCompleteSet[ioRequest.Id]

    def ReleaseIORequest(self, ioRequest):
        with Locking(self._ioCompleteSetLock):
            if ioRequest.Id in self._ioCompleteSet:
                self._ioCompleteSet.pop(ioRequest.Id)

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
        self._ioCompleteSet[ioRequest.Id].set()

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
            self._logger.info('now creating')
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
