import cPickle as pickle

class SimpleIndex:
    '''SimpleIndex Structure: TermId-DocId1-DocId2-DocId3
       doesn't contain any relavance score'''
    def __init__(self):
        self._indexMap = {}

    # make unit test happy
    def add(self, termId, index):
        assert (isinstance(termId, int) and isinstance(index, set))
        self._indexMap[termId] = index

    def add_termid_docid(self, termId, docid):
        if termId not in self._indexMap:
            self._indexMap[termId] = set()
        self._indexMap[termId].add(docid)

    def get_indexmap(self):
        return self._indexMap

    def get_index(self, termId):
        if termId in self._indexMap:
            return self._indexMap[termId]
        else:
            return set()

class SimpleIndexHandler:
    def __init__(self, simpleIndex):
        assert isinstance(simpleIndex, SimpleIndex)
        self._simpleIndex = simpleIndex
        self._termIds = []

    def clear(self):
        self._termIds = []

    def add(self, termId):
        self._termIds.append(termId)

    def intersect(self):
        assert len(self._termIds) >= 2
        lastIndex = self._simpleIndex.get_index(self._termIds[0])
        for i in range(1, len(self._termIds)):
            lastIndex &= self._simpleIndex.get_index(self._termIds[i])
        return lastIndex

    def union(self):
        assert len(self._termIds) >= 2
        lastIndex = self._simpleIndex.get_index(self._termIds[0])
        for i in range(1, len(self._termIds)):
            lastIndex |= self._simpleIndex.get_index(self._termIds[i])
        return lastIndex

class SimpleIndexReader:
    def read(self, indexFileName):
        with open(indexFileName, 'rb') as indexMapFile:
            index = pickle.loads(indexMapFile.read())
        assert isinstance(index, SimpleIndex) == True
        return index

class SimpleIndexWriter:
    def write(self, indexMap, indexFileName):
        assert isinstance(indexMap, SimpleIndex)
        # TODO add a MD5 to filename
        # use binary format
        indexMapToStore = pickle.dumps(indexMap, True)
        with open(indexFileName, 'wb') as indexFile:
            indexFile.write(indexMapToStore)
