#!/usr/bin/python

import sys
sys.path.append('../common/SimpleIndex')
sys.path.append('../indexer/')

from IndexServingHandler import IndexSearcher
from IndexServingHandler import IndexServingHandler
from SimpleIndex import *
from TermIdMapping import TermIdMappingHandler as TermMapHandler

if __name__ == '__main__':
    reader = SimpleIndexReader()
    index = reader.read('../index_chunk/testIndex')
    searcher = IndexSearcher(index)
    termIdList = [36, 52]
    searcher.search(termIdList)

    handler = IndexServingHandler(index)
    termidMapping = TermMapHandler.read_termid_mapping(
                        '../index_chunk/testTermidMapping')
    handler.load_debug_mapping(termidMapping)
    handler.ping()
    handler.search(termIdList)
    termsList = ['action', 'account']
    handler.search_terms(termsList)
