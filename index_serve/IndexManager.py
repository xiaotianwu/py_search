from common.Cache import Cache
from common.DiskIOManager import DiskIOManagerThread
from common.Logger import Logger
from common.uncompress_index_dealer.UncompressIndex import *
from common.plain_file_dealer.PlainFile import *

class IndexManager:
    '''if mem is not enough, load high-frequency item to main
       memory and put a part of low-freq item in LRU cache'''
    # TODO enable cache after creating more index
    def __init__(self, cacheSize, diskIOThreadNum):
        self._mainIndex = None
        self._swapIndex = Cache(cacheSize) 
        self._diskIOManager = DiskIOManagerThread(diskIOThreadNum)
        self._diskIOManager.start()
        self._allReady = False

    # TODO create a manage mechanism supporting multiple index file
    def Init(self, mainIndexFile, swapIndexFile = None):
        self.InitMainIndex(mainIndexFile)
        self.InitSwapIndex(swapIndexFile)
        self._allReady = True
        
    def InitMainIndex(self, indexFile):
        req = UncompressIndexIORequest('READALL', indexFile)
        readFinished = self._diskIOManager.PostIORequest(req)
        # main index file must load sync
        readFinished.wait()
        self._mainIndex = req.result
        if not isinstance(self._mainIndex, UncompressIndex):
            raise Exception('not UncompressIndex')
        print 'finish init main index'

    def InitSwapIndex(self, indexFile):
        pass

    def Fetch(self, termId):
        '''fetch index from main chunk first, then LRU cache
           then disk, if disk hit, load it to LRU cache'''
        index = self._mainIndex.Fetch(termId)
        if index != None:
            return (index, True) # modify True/False to retCode
        #index = self._swapIndex.Fetch(termId)
        #if index != None:
        #    return (index, True)
        #else:
        #    return (None, False)
        #index = diskio result
        #return index, retCode

    def Stop(self):
        self._diskIOManager.PostStopRequest()

    def GetMainIndex(self):
        '''method for test'''
        return self._mainIndex.GetIndexmap()

    def GetSwapIndex(self):
        '''method for test'''
        return self._swapIndex

    def IsReady(self):
        return self._allReady
