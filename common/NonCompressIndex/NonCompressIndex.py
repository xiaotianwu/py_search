import cPickle as pickle

class NonCompressIndex:
    '''NonCompressIndex Structure: Dict
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

# NonCompressIndex File Struct
# PostingList1(TermId1,docid1,score1,docid2,score2...), PostingList2,...
# Dict of Offset for PostingList
# TermId1, Offset of PostingList1
# TermId2, Offset of PostingList2...
# MD5 checksum

class NonCompressIndexWriter:
    def write(self, indexMap, indexFileName):
        if not isinstance(indexMap, NonCompressIndex):
            raise TypeError('input must be NonCompressIndex')
        # TODO add a MD5 to filename
        indexFile = open(indexFileName, 'wb')
        offset = 0
        indexOffsetMap = {}
        # write term-postinglist pair first
        for (k, v) in indexMap.get_indexmap().items():
            postingList = pickle.dumps((k, v), True)
            indexFile.write(postingList)
            indexOffsetMap[k] = (offset, len(postingList))
            offset += len(postingList)
        offsetMap = pickle.dumps(indexOffsetMap, True);
        # then offset map
        indexFile.write(offsetMap)
        offsetMapSize = int(len(offsetMap))
        indexFile.write(offsetMapSize)
        indexFile.close()
 
class NonCompressIndexReader:
    def read(self, indexFileName):
        intLen = int(0).__sizeof__()
        # load offset map first
        indexMapFile = open(indexFileName, 'rb')
        indexMapFile.seek(0 - intLen, 2)
        offsetMapSize = indexMapFile.read(intLen)
        indexMapFile.seek(0 - intLen - offsetMapSize, 2)
        offsetMap = pickle.loads(indexMapFile.read(offsetMapSize))
        # then postinglist
        # TODO make the storage of index offset sequentially
        index = NonCompressIndex()
        for (termid, offset) in offsetMap:
            indexMapFile.seek(offset[0], 0)
            index.add(termid, pickle.loads(indexMapFile.read(offset[1]))
        indexMapFile.close()
        return index

class NonCompressIndexHandler:
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
