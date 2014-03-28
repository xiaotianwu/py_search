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

class PostingList(Structure):
    _fields_ = [('list', POINTER(DocScorePair)),
                ('len', c_uint)]

class UncompressIndex:
    def __init__(self):
        self._indexMap = {}

    def Add(self, termId, index):
        if termId not in self._indexMap:
            self._indexMap[termId] = index
        else:
            self._indexMap[termId] |= index

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

class UncompressIndexHandler:
    def __init__(self):
        self._indexContainer = []

    def Clear(self):
        self._indexContainer = []

    def Add(self, index):
        self._indexContainer.append(index)

    def Intersect(self):
        if len(self._indexContainer) == 1:
            return self._indexContainer[0]
        uncompressIndexLib.Intersect()
