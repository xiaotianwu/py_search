import os
from ctypes import *

rootPath = os.environ['PY_SEARCH_ROOT']
uncompressIndexLibPath = rootPath + '/libc/uncompress_index'
uncompressIndexLib = CDLL(uncompressIndexLibPath + '/UncompressIndex.so')

class DocScorePair(Structure):
    _fields_ = [('docid', c_uint)]

class DocidSet(Structure):
    _fields_ = [('docids', POINTER(c_uint)),
                ('len', c_uint)]

    def Print(self):
        uncompressIndexLib.PrintDocidSet(self)

class PostingList(Structure):
    _fields_ = [('len', c_uint),
                ('list', POINTER(DocScorePair))]

class UncompressIndex:
    def __init__(self):
        self._indexMap = {}

    def Add(self, termId, postingList):
        if not isinstance(postingList, PostingList):
            raise Exception('unsupported index type')
        if postingList.list == None or postingList.len <= 0:
            return
        if termId not in self._indexMap:
            self._indexMap[termId] = postingList
        #else:
            # call merge in libc

    def AddTermDocPair(self, termId, docid):
        pass

    def GetIndexMap(self):
        return self._indexMap

    def Fetch(self, termId):
        if termId in self._indexMap:
            return self._indexMap[termId]
        else:
            return None

class UncompressIndexWriter:
    def __init__(self):
        self._logger = Logger.Get('UncompressIndexWriter')

    def Write(self, indexMap, indexFileName):
        if not isinstance(indexMap, UncompressIndex):
            raise TypeError('input must be UncompressIndex')
        self._logger.info('write UncompressIndex file: ' + indexFileName)
        indexFile = open(indexFileName, 'wb')
        offset = 0
        indexOffsetMap = {}

        # write term-postinglist pair first
        # TODO make the storage of index offset sequentially
        for (term, postingList) in indexMap.GetIndexMap().items():
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('write termid = %s, postingList = %d'
                                   % (term, postingList))
            #pickle.dump(postingList, indexFile, 2)
            length = indexFile.tell() - offset
            indexOffsetMap[term] = (offset, length)
            offset = indexFile.tell()
        self._logger.info('index write finished')

        # then offset map
        pickle.dump(indexOffsetMap, indexFile, 2);
        offsetMapSize = str(indexFile.tell() - offset)
        self._logger.info('offset map write len: ' + offsetMapSize)
        offsetMapSize = LeftPadding(offsetMapSize, UINT32_STR_LEN)
        indexFile.write(offsetMapSize)

        # TODO need checksum
        indexFile.close()
        self._logger.info('finish write')

class UncompressIndexHandler:
    def __init__(self, postingListUpperBound = 15):
        PostingListArray = PostingList * postingListUpperBound
        self._listContainer = PostingListArray()
        self._listContainerSize = 0
        self._listUpperBound = postingListUpperBound

    def Clear(self):
        self._listContainerSize = 0

    def Add(self, postingList):
        if self._listContainerSize > self._listUpperBound:
            raise Exception('too many postinglist')
        self._listContainer[self._listContainerSize] = postingList
        self._listContainerSize += 1

    def Intersect(self):
        result = DocidSet()
	uncompressIndexLib.Intersect(self._listContainer,
                                     self._listContainerSize,
                                     pointer(result))
        return result
