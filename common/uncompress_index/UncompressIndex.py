import cPickle as pickle
import os
import logging
import mmap
from threading import Lock

from common.Common import LeftPadding
from common.Common import Locking
from common.Logger import Logger
from common.IORequestType import IORequest

class UncompressIndex:
    '''UncompressIndex Structure: Dict
       Key: TermId
       Value: (DocId1, ScoreOfDoc1), (DocId2, ScoreOfDoc2), ...'''

    def __init__(self):
        self._indexMap = {}

    def Add(self, termId, index):
        if termId not in self._indexMap:
            self._indexMap[termId] = index
        else:
            self._indexMap[termId] += index

    def AddTermDocPair(self, termId, docid):
        if termId not in self._indexMap:
            self._indexMap[termId] = set()
        self._indexMap[termId].add(docid)

    def GetIndexMap(self):
        return self._indexMap

    def Fetch(self, termId):
        if termId in self._indexMap:
            return self._indexMap[termId]
        else:
            return None

# UncompressIndex File Struct
# File Begin
# [PostingList]
# PostingList1(TermId1: docid1,score1,docid2,score2...),
# PostingList2(TermId2: docid1,score1,docid2,score2...),
# ...
# [Dict of postinglist offset]
# TermId1, Offset of PostingList1
# TermId2, Offset of PostingList2
# ...
# length of dict
# File End
UINT32_STR_LEN= 32

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
        for (term, index) in indexMap.GetIndexMap().items():
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('write termid = ' + str(term) +
                                   ' index = ' + str(index))
            postingList = pickle.dump(index, indexFile, 2)
            length = indexFile.tell() - offset
            indexOffsetMap[term] = (offset, length)
            offset = indexFile.tell()
        self._logger.info('index write finished')

        # then offset map
        offsetMap = pickle.dump(indexOffsetMap, indexFile, 2);
        offsetMapSize = str(indexFile.tell() - offset)
        self._logger.info('offset map write len: ' + offsetMapSize)
        offsetMapSize = LeftPadding(offsetMapSize, UINT32_STR_LEN)
        indexFile.write(offsetMapSize)

        # TODO need checksum
        indexFile.close()
        self._logger.info('finish write')
 
class UncompressIndexReader:
    def __init__(self, isMMap = False):
        self._logger = Logger.Get('UncompressIndexReader')
        self._offsetMap = None
        self._indexFileDesc = None
        self._indexFileMMap = None
        self._isMMap = isMMap
        self._indexFileName = None
        self._fileLock = Lock()

    def Open(self, indexFileName):
        '''open index file and get the mapping of postingList offset'''
        '''open is not thread-safe'''
        self._logger.info('open UncompressIndex file: ' + indexFileName +
                          'mmap: ' + str(self._isMMap))
        self._indexFileName = indexFileName
        self._indexFileDesc = open(indexFileName, 'r')
        if self._isMMap == True:
            self._indexFileMMap = mmap.mmap(self._indexFileDesc.fileno(), 0,
                                            prot = mmap.PROT_READ)
            self._indexFileMMap.seek(-UINT32_STR_LEN, 2)
            offsetMapSize = int(self._indexFileMMap.read(UINT32_STR_LEN))
            self._logger.info('read offset map len: ' + str(offsetMapSize))

            self._indexFileMMap.seek(0 - UINT32_STR_LEN - offsetMapSize, 2)
            self._offsetMap = pickle.loads(self._indexFileMMap.read(offsetMapSize))
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('self._offsetMap = ' + str(self._offsetMap))
            self._logger.info('offset map read finished')
            if not isinstance(self._offsetMap, dict):
                raise TypeError('offset map read failed')
        else:
            self._indexFileDesc.seek(-UINT32_STR_LEN, 2)
            offsetMapSize = int(self._indexFileDesc.read(UINT32_STR_LEN))
            self._logger.info('read offset map len: ' + str(offsetMapSize))

            self._indexFileDesc.seek(0 - UINT32_STR_LEN - offsetMapSize, 2)
            self._offsetMap = pickle.loads(self._indexFileDesc.read(offsetMapSize))
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('self._offsetMap = ' + str(self._offsetMap))
            self._logger.info('offset map read finished')
            if not isinstance(self._offsetMap, dict):
                raise TypeError('offset map read failed')

    def ReadAll(self):
        '''get the entire UncompressIndex from the file'''
        index = UncompressIndex()
        with Locking(self._fileLock):
            for (termid, value) in self._offsetMap.items():
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug('read termid = ' + str(termid) +
                                       ' (value, len) = ' + str(value))
                if self._isMMap == True:
                    self._indexFileMMap.seek(value[0], 0)
                    postingList = pickle.loads(self._indexFileMMap.read(value[1]))
                else:
                    self._indexFileDesc.seek(value[0], 0)
                    postingList = pickle.loads(self._indexFileDesc.read(value[1]))
                if not isinstance(postingList, set):
                    raise TypeError('postingList for ' +
                                    str(termid) + ' open failed')
                index.Add(termid, postingList)
            self._logger.info('finish read')
        return index

    def Read(self, termid):
        '''read specified postinglist by term id'''
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('read termid: ' + str(termid) +
                               ' from indexFile: ' + self._indexFileName)
        offset = self._offsetMap[termid][0]
        length = self._offsetMap[termid][1]
        if termid in self._offsetMap:
            with Locking(self._fileLock):
                if self._isMMap == True:
                    self._indexFileMMap.seek(offset, 0)
                    binaryData = self._indexFileMMap.read(length)
                else:
                    self._indexFileDesc.seek(offset, 0)
                    binaryData = self._indexFileDesc.read(length)
            return pickle.loads(binaryData)
        else:
            self._logger.error('termid: ' + str(termid) +
                               ' not in indexFile: ' + self._indexFileName)
            return None

    def DoRequest(self, ioRequest):
        if ioRequest.type == 'READ':
            return self.Read(ioRequest.key)
        elif ioRequest.type == 'READALL':
            return self.ReadAll()
        else:
            raise Exception('unsupported request type ' + ioRequest.type)

    def Close(self):
        '''close is not thread safe'''
        del self._offsetMap
        self._offsetMap = None
        if self._indexFileMMap != None:
            self._indexFileMMap.close()
        self._indexFileDesc.close()
        self._indexFileMMap = None
        self._indexFileDesc = None
        self._logger.info('close UncompressIndex file: ' +
                          self._indexFileName)
        self._indexFilename = None

class UncompressIndexHandler:
    def __init__(self):
        self._indexContainer = []

    def Clear(self):
        self._indexContainer = []

    def Add(self, index):
        self._indexContainer.append(index)

    def Intersect(self):
        assert len(self._indexContainer) >= 2
        result = self._indexContainer[0] & self._indexContainer[1]
        for i in range(2, len(self._indexContainer)):
            result &= self._indexContainer[i]
        return result

    def Union(self):
        assert len(self._indexContainer) >= 2
        result = self._indexContainer[0] | self._indexContainer[1]
        for i in range(2, len(self._indexContainer)):
            result |= self._indexContainer[i]
        return result

class UncompressIndexMerger:
    def __init__(self):
        self._indexToMergeList = []

    def Add(self, index):
        self._indexToMergeList.append(index)

    def DoMerge(self):
        mergedIndex = UncompressIndex()
        for index in self._indexToMergeList:
            for termId in index.GetIndexMap().keys():
                mergedIndex.Add(termId, index.Fetch(termId))
        return mergedIndex
