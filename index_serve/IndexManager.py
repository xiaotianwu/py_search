import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from Cache import Cache
from DiskIOManager import DiskIORequest
from DiskIOManager import DiskIOManager
from Logger import Logger
from SimpleIndex import SimpleIndexReader

class IndexManager:
       '''if mem is not enough, load high-frequency item to main mem
          and put them in LRU cache'''
    def __init__(self, cacheSize, diskIOThreadNum):
        self._indexCache = Cache(cacheSize)
        self._diskIOManager = DiskIOManager(diskIOThreadNum)
        self._indexReader = SimpleIndexReader() # TODO replace it with commonReader
        self._ready = False

    def init(self, indexFiles):
        for inFile in indexFiles:
            self.sync_load(inFile)
        self._ready = True
        
    def fetch(self, termId):
        '''fetch index from cache first, if it
           doesn't exist, load it from disk'''
        index = self._indexCache.fetch(termId)
        if index is not None:
            return index, True
        else:
            return None, False # TODO add a caller to DiskIO

    def fetch_by_term(self, term):
        '''this is a test method'''
        #termid = get_id_from_term(term)
        #return get_index(termId)
        pass

    def sync_load(self, fileName):
        indexMap = self._indexReader.read(fileName)
        for (k, v) in indexMap:
            self._indexCache.add(k, v)

    def async_load(self, fileName):
        pass
