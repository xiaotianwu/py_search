import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from Cache import Cache
from DiskIOManager import DiskIORequest
from DiskIOManager import DiskIOManager
from Logger import Logger
from SimpleIndex import SimpleIndexReader

class IndexManager:
    '''if mem is not enough, load high-frequency item to main
       memory and put a part of low-freq item in LRU cache'''
    # TODO enable cache after creating more index
    def __init__(self, cacheSize = 0, diskIOThreadNum = 1):
        self._mainIndex = None
        self._swapIndex = Cache(cacheSize) 
        self._diskIOManager = DiskIOManager(diskIOThreadNum)
        # TODO replace it with commonReader
        self._indexReader = SimpleIndexReader() 
        self._allReady = False

    # TODO create a manage mechanism supporting when multiple index file
    def init(self, mainIndexFile):
        self.init_main_index(mainIndexFile)
        self.init_swap_index()
        self._allReady = True
        
    def init_main_index(self, indexFile):
        self._mainIndex = self._indexReader.read(indexFile)

    def init_swap_index(self, indexFile = None):
        pass

    def fetch(self, termId):
        '''fetch index from main chunk first, then LRU cache
           then disk, if disk hit, load it to LRU cache'''
        index = self._mainIndex.fetch(termId)
        if index != None:
            return index, True # modify True/False to retCode
        index = self._swapIndex.fetch(termId)
        if index != None:
            return index, True
        else:
            return None, False
        #index = diskio result
        #return index, retCode

    def fetch_by_term(self, term):
        '''this is a test method'''
        #termid = get_id_from_term(term)
        #return get_index(termId)
        pass

    def is_ready(self):
        return self._allReady
