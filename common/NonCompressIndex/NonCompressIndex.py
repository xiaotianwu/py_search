import cPickle as pickle

class NonCompressIndex:
    '''NonCompressIndex Structure: Dict
       Key: TermId
       Value: (DocId1, ScoreOfDoc1), (DocId2, ScoreOfDoc2), ...'''

    __slots__ = ['_indexMap', '_minDocId', '_maxDocId']

    def __init__(self):
        self._indexMap = {}
        self._maxDocId = -1
        self._minDocId = 2 << 64

    # make unit test happy
    def add(self, termId, index):
        if not isinstance(termId, int) and isinstance(index, set):
            raise TypeError('termId must be int and index must be set')
        for i in index:
            if len(i) < 2:
                continue
            if i[0] > self._maxDocId:
                self._maxDocId = i[0]
            if i[0] < self._minDocId:
                self._minDocId = i[0]
        self._indexMap[termId] = index

    def add_termid_docid(self, termId, docid):
        if termId not in self._indexMap:
            self._indexMap[termId] = set()
        self._indexMap[termId].add(docid)
        if docid > self._maxDocId:
            self._maxDocId = docid
        if docid < self._minDocId:
            self._minDocId = docid

    def get_indexmap(self):
        return self._indexMap

    def fetch(self, termId):
        if termId in self._indexMap:
            return self._indexMap[termId]
        else:
            return None

class NonCompressIndexReader:
    def read(self, indexFileName):
        with open(indexFileName, 'rb') as indexMapFile:
            index = pickle.loads(indexMapFile.read())
        assert isinstance(index, NonCompressIndex) == True
        return index

class NonCompressIndexWriter:
    def write(self, indexMap, indexFileName):
        if not isinstance(indexMap, NonCompressIndex):
            raise TypeError('input must be NonCompressIndex')
        # TODO add a MD5 to filename
        # use binary format
        indexMapToStore = pickle.dumps(indexMap, True)
        with open(indexFileName, 'wb') as indexFile:
            indexFile.write(indexMapToStore)

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
