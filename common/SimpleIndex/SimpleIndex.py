import cPickle as pickle

class SimpleIndex:
    def __init__(self, indexMap = dict()):
        assert isinstance(indexMap, dict)
        self._indexMap = indexMap

    # make unit test happy
    def add(self, term, index):
        assert (isinstance(term, str) and isinstance(index, set))
        self._indexMap[term] = index

    def add_term_docid(self, term, docid):
        if term not in self._indexMap:
            self._indexMap[term] = set()
        self._indexMap[term].add(docid)

    def get_indexmap(self):
        return self._indexMap

    def get_index(self, term):
        if term in self._indexMap:
            return self._indexMap[term]
        else:
            return set()

class SimpleIndexHandler:
    def __init__(self, simpleIndex):
        assert isinstance(simpleIndex, SimpleIndex)
        self._simpleIndex = simpleIndex
        self._terms = []

    def clear(self):
        self._terms.clear()

    def add(self, term):
        self._terms.append(term)

    def intersect(self):
        assert len(self._terms) >= 2
        lastIndex = self._simpleIndex.get_index(self._terms[0])
        for i in range(1, len(self._terms)):
            lastIndex &= self._simpleIndex.get_index(self._terms[i])
        return lastIndex

    def union(self):
        assert len(self._terms) >= 2
        lastIndex = self._simpleIndex.get_index(self._terms[0])
        for i in range(1, len(self._terms)):
            lastIndex |= self._simpleIndex.get_index(self._terms[i])
        return lastIndex

class SimpleIndexReader:
    def read(self, indexFileName):
        indexMapFile = open(indexFileName, 'rb')
        index = pickle.loads(indexMapFile.read())
        indexMapFile.close()
        assert isinstance(index, SimpleIndex)
        return index

class SimpleIndexWriter:
    def write(self, indexMap, indexFileName):
        assert isinstance(indexMap, SimpleIndex)
        # TODO add a MD5 to filename
        indexMapToStore = pickle.dumps(indexMap, True) # use binary format
        indexFile = open(indexFileName, 'wb')
        indexFile.write(indexMapToStore)
        indexFile.close()
