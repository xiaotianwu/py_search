from common.Logger import Logger

from IndexBlockManager import IndexBlockManager
from IndexConfig import IndexReaderFactory
from IndexConfig import IndexWriterFactory
from IndexConfig import IndexMergerFactory
from IndexIOManager import IndexIOManagerThread
from IndexIOManager import IndexIORequest

class IndexManager:
    def __init__(self, cacheSize, diskIOThreadNum,
                 indexFolder, indexMappingstr):
        self._index = None
        self._allReady = False
        self._indexIOManager = IndexIOManagerThread(cacheSize, diskIOThreadNum)
        self._indexIOManager.start()
        self._indexBlockManager = IndexBlockManager(indexFolder, indexMappingstr)
        self._InitIndex()
        self._allReady = True

    def _InitIndex(self):
        readEvents = []
        allBlocks = self._indexBlockManager.GetAllBlocks()
        for block in allBlocks:
            if block.type == 'mem':
               req = IndexIORequest('READALL', block.mappingFile)
               readEvents.append(self._IndexIOManager.PostIORequest(req))
        merger = IndexMergerFactory.Get()
        # mem index loading is sync
        for event in readEvents:
            event.wait()
            merger.Add(event.result)
        self._index = merger.DoMerge()
        for event in readEvents:
            del event.result
        del readEvents

    def Fetch(self, termId):
        index = self._index.Fetch(termId)
        if index != None:
            return (index, True)
        else:
            block = self._indexBlockManager.GetBlock(termId)
            if block == None:
                return (None, False)
            req = IndexIORequest('READ', block.mappingFile, termId)
            readEvent = self._indexIOManager.PostIORequest(req)
            return (readEvent, False)

    def Stop(self):
        self._indexIOManager.PostStopRequest()
        self._indexIOManager.join()

    def GetMainIndex(self):
        '''method for test'''
        return self._mainIndex.GetIndexmap()
        
    def IsReady(self):
        return self._allReady
