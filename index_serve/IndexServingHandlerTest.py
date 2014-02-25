#!/usr/bin/python

import sys
sys.path.append('../common/SimpleIndex')

from IndexServingHandler import IndexSearcher
from SimpleIndex import *

if __name__ == '__main__':
    reader = SimpleIndexReader()
    index = reader.read('../index_chunk/testIndex')
    searcher = IndexSearcher(index)
    termList = ['music', 'military']
    searcher.search(termList)
