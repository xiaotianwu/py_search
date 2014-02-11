import sys
sys.path.append('..')

from InvertedIndex import *

class SimpleInvertedIndex(InvertedIndex):
    term = ''
    index = []

    def __init__(self, term, index):
        self.index = index
        self.term = term

class SimpleInvertedIndexHandler(InvertedIndexHandler):
    def __init__(self):
        pass

    def intersect(self, index1, index2):
        return list(set(index1.index) & set(index2.index))

    def union(self, index1, index2):
        return list(set(index1.index) | set(index2.index))
