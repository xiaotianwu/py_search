from common.Cache import Cache
from common.Common import Locking
from common.DiskIOManager import DiskIOManagerThread
from common.Logger import Logger
from common.uncompress_index.UncompressIndex import *
from common.IORequestType import IORequest
from IndexMergeManager import IndexMergeManager

class IndexManager:
    def __init__(self, cacheSize, diskIOThreadNum):
        self._index = None
        self._allReady = False
        self._diskIOManager = DiskIOManagerThread(cacheSize, diskIOThreadNum)
        self._diskIOManager.start()
        self._termIdToFile = {}

    # TODO create a manage mechanism supporting multiple index file
    def Init(self, indexFiles):
        self.InitIndex(indexFiles)
        self._allReady = True
        
    def InitIndex(self, indexFiles):
        '''main index loading is sync'''
        mainIndexEvents = []
        for index in indexFiles:
            if index[1] == 'main':
               req = IORequest('READALL', index[0])
               mainIndexEvents.append(self._diskIOManager.PostIORequest(req))
        mainIndexMerger = IndexMergeManager(UncompressIndexMerger())
        for event in mainIndexEvents:
            event.wait()
            mainIndexMerger.Add(event.result)
        self._mainIndex = mainIndexMerger.DoMerge()
        if not isinstance(self._mainIndex, UncompressIndex):
            raise Exception('not UncompressIndex')
        print 'initialze of main index finished'

    def Fetch(self, termId):
        index = self._mainIndex.Fetch(termId)
        if index != None:
            return (index, True)
        else:
            if termId in self._termIdToFile:
                req = IORequest('READ', self._termIdToFile[termId], termId)
                readEvent = DiskIOManagerThread.PostIORequest(req)
                return (readEvent, False)
            else:
                return (None, False)

    def Stop(self):
        self._diskIOManager.PostStopRequest()
        self._diskIOManager.join()

    def GetMainIndex(self):
        '''method for test'''
        return self._mainIndex.GetIndexmap()
        
    def IsReady(self):
        return self._allReady
