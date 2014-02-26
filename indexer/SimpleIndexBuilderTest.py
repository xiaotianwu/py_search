#!/usr/bin/python
import sys
import os
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from DocIdMapping import DocIdMappingHandler as DocIdMap
from TermIdMapping import TermIdMappingHandler as TermIdMap
from SimpleIndexBuilder import SimpleIndexBuilder
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader

if __name__ == '__main__':
    path = '../page_chunk/'
    docidMappingFile = '../index_chunk/testDocidMapping'
    termidMappingFile = '../index_chunk/testTermidMapping'
    stopwordsFile = '../common/StopWordsList.txt'
    termsListFile = 'terms.txt'
    indexFile = '../index_chunk/testIndex'
    
    DocIdMap.build_docid_mapping(path, docidMappingFile)
    TermIdMap.build_termid_mapping(termsListFile, termidMappingFile)

    builder = SimpleIndexBuilder()
    builder.init(docidMappingFile, termidMappingFile, stopwordsFile)
    builder.build_index(path, indexFile)
    
    reader = SimpleIndexReader()
    index = reader.read(indexFile)
    readableFileName = '../index_chunk/readableIndex'
    with open(readableFileName, 'w') as f:
        for (k, v) in index.get_indexmap().items():
            f.write(str(k) + '\n' + str(v) + '\n')
