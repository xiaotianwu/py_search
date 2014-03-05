import cPickle as pickle
import threading

class SimpleIndex:
    '''SimpleIndex Structure: TermId-DocId1-DocId2-DocId3
       doesn't contain any relavance score'''
    def __init__(self):
        self._indexMap = {}

    # make unit test happy
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

class SimpleIndexHandler:
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

class SimpleIndexReader:
    def read(self, indexFileName):
        with open(indexFileName, 'rb') as indexMapFile:
            index = pickle.loads(indexMapFile.read())
        assert isinstance(index, SimpleIndex) == True
        return index

class SimpleIndexWriter:
    def write(self, indexMap, indexFileName):
        if not isinstance(indexMap, SimpleIndex):
            raise TypeError('input must be SimpleIndex')
        # TODO add a MD5 to filename
        # use binary format
        indexMapToStore = pickle.dumps(indexMap, True)
        with open(indexFileName, 'wb') as indexFile:
            indexFile.write(indexMapToStore)
