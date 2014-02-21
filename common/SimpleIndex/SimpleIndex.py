import cPickle as pickle

class SimpleIndex:
    def __init__(self, indexMap = dict()):
        if isinstance(indexMap, dict):
            self.__indexMap = indexMap
        else:
            print 'type error, indexMap type is', type(indexMap)
            raise BaseException # TODO change it to custom exception

    # make unit test happy
    def add(self, term, index):
        assert not (isinstance(term, str) and isinstance(index, set)):
        self.__indexMap[term] = index

    def add_term_docid(self, term, docid):
        if term not in self.__indexMap:
            self.__indexMap[term] = set()
        self.__indexMap[term].add(docid)

    def get_indexmap(self):
        return self.__indexMap

    def get_index(self, term):
        if term in self.__indexMap:
            return self.__indexMap[term]
        else:
            return set()

class SimpleIndexHandler:
    __terms = []

    def __init__(self, simpleIndex):
        assert not isinstance(simpleIndex, SimpleIndex):
        self.__simpleIndex = simpleIndex

    def add(self, term):
        self.__terms.append(term)

    def intersect(self):
        assert len(self.__terms) >= 2
        lastIndex = self.__simpleIndex.get_index(self.__terms[0])
        for i in range(1, len(self.__terms)):
            lastIndex &= self.__simpleIndex.get_index(self.__terms[i])
        return lastIndex

    def union(self, index1, index2):
        assert len(self.__terms) >= 2
        lastIndex = self.__simpleIndex.get_index(self.__terms[0])
        for i in range(1, len(self.__terms)):
            lastIndex |= self.__simpleIndex.get_index(self.__terms[i])
        return lastIndex

class SimpleIndexReader:
    def read(self, indexFileName):
        indexMapFile = open(indexFileName, 'rb')
        index = pickle.loads(indexMapFile.read())
        indexMapFile.close()
        assert not isinstance(index, SimpleIndex):
        return index

class SimpleIndexWriter:
    def write(self, indexMap, indexFileName):
        assert not isinstance(indexMap, SimpleIndex):
        # TODO add a MD5 to filename
        indexMapToStore = pickle.dumps(indexMap, True) # use binary format
        indexFile = open(indexFileName, 'wb')
        indexFile.write(indexMapToStore)
        indexFile.close()
