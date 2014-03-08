import cPickle as pickle
import sys
sys.path.append('..')

from Common import left_padding
from Logger import Logger

class UncompressIndex:
    '''UncompressIndex Structure: Dict
       Key: TermId
       Value: (DocId1, ScoreOfDoc1), (DocId2, ScoreOfDoc2), ...'''

    def __init__(self):
        self._indexMap = {}

    def add(self, termId, index):
        if not isinstance(termId, int) and isinstance(index, set):
            raise TypeError('termId must be int and index must be set')
        self._indexMap[termId] = index

    def add_termid_docid(self, termId, docid):
        if termId not in self._indexMap:
            self._indexMap[termId] = set()
        self._indexMap[termId].add(docid)

    def get_indexmap(self):
        return self._indexMap

    def fetch(self, termId):
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
        self._logger = Logger.get('UncompressIndexWriter')

    def write(self, indexMap, indexFileName):
        if not isinstance(indexMap, UncompressIndex):
            raise TypeError('input must be UncompressIndex')
        self._logger.info('write UncompressIndex file: ' + indexFileName)
        indexFile = open(indexFileName, 'wb')
        offset = 0
        indexOffsetMap = {}

        # write term-postinglist pair first
        for (term, index) in indexMap.get_indexmap().items():
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
        offsetMapSize = left_padding(offsetMapSize, UINT32_STR_LEN)
        indexFile.write(offsetMapSize)

        # TODO need checksum
        indexFile.close()
        self._logger.info('finish write')
 
class UncompressIndexReader:
    def __init__(self):
        self._logger = Logger.get('UncompressIndexReader')

    def read(self, indexFileName):
        # load offset map first
        self._logger.info('read UncompressIndex file: ' + indexFileName)
        indexMapFile = open(indexFileName, 'rb')
        indexMapFile.seek(-UINT32_STR_LEN, 2)
        offsetMapSize = int(indexMapFile.read(UINT32_STR_LEN))
        self._logger.info('read offset map len: ' + str(offsetMapSize))

        indexMapFile.seek(0 - UINT32_STR_LEN - offsetMapSize, 2)
        offsetMap = pickle.loads(indexMapFile.read(offsetMapSize))
        self._logger.debug('offsetMap = ' + str(offsetMap))
        self._logger.info('offset map read finished')
        if not isinstance(offsetMap, dict):
            raise TypeError('offset map read failed')

        # then postinglist
        # TODO make the storage of index offset sequentially
        index = UncompressIndex()
        for (termid, offset) in offsetMap.items():
            self._logger.debug('read termid = ' + str(termid) +
                               ' (offset, len) = ' + str(offset))
            indexMapFile.seek(offset[0], 0)
            postingList = pickle.loads(indexMapFile.read(offset[1]))
            if not isinstance(postingList, set):
                raise TypeError('postingList for ' +
                                str(termid) + ' load failed')
            index.add(termid, postingList)

        indexMapFile.close()
        self._logger.info('finish read')
        return index

class UncompressIndexHandler:
    def __init__(self):
        self._indexContainer = []

    def clear(self):
        self._indexContainer = []

    def add(self, index):
        self._indexContainer.append(index)

    def intersect(self):
        assert len(self._indexContainer) >= 2
        result = self._indexContainer[0] & self._indexContainer[1]
        for i in range(2, len(self._indexContainer)):
            result &= self._indexContainer[i]
        return result

    def union(self):
        assert len(self._indexContainer) >= 2
        result = self._indexContainer[0] | self._indexContainer[1]
        for i in range(2, len(self._indexContainer)):
            result |= self._indexContainer[i]
        return result
