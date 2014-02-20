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
        if isinstance(term, str) and isinstance(index, set):
            self.__indexMap[term] = index
        else:
            print 'type error, term type is', type(term), 'index type is', type(index)
            raise BaseException # TODO change it to custom exception

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
    def __init__(self, simpleIndex):
        if isinstance(simpleIndex, SimpleIndex):
            self.__simpleIndex = simpleIndex
        else:
            print 'type error, index type is', type(simpleIndex)
            raise BaseException # TODO change it to custom exception

    def intersect(self, term1, term2):
        index1 = self.__simpleIndex.get_index(term1)
        index2 = self.__simpleIndex.get_index(term2)
        return index1 & index2

    def union(self, index1, index2):
        index1 = self.__simpleIndex.get_index(term1)
        index2 = self.__simpleIndex.get_index(term2)
        return index1 | index2

class SimpleIndexReader:
    def read(self, indexFileName):
        indexMapFile = open(indexFileName, 'rb')
        index = pickle.loads(indexMapFile.read())
        indexMapFile.close()
        if not isinstance(index, SimpleIndex):
            print 'type error, file type is not SimpleIndex'
            raise BaseException # TODO change it to custom exception
        return index

class SimpleIndexWriter:
    def write(self, indexMap, indexFileName):
        if not isinstance(indexMap, SimpleIndex):
            print 'type error, indexMap type is', type(indexMap)
            raise BaseException # TODO change it to custom exception
        # TODO add a MD5 to filename
        indexMapToStore = pickle.dumps(indexMap, True) # use binary format
        indexFile = open(indexFileName, 'wb')
        indexFile.write(indexMapToStore)
        indexFile.close()
