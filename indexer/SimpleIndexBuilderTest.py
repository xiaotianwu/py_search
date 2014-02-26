#!/usr/bin/python
import sys
import os
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from DocIdMappingGen import DocIdMappingGen as Generator
from SimpleIndexBuilder import SimpleIndexBuilder
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader

if __name__ == '__main__':
    path = '../page_chunk/'
    mappingFileName = '../index_chunk/testMapping'
    indexFileName = '../index_chunk/testIndex'
    
    Generator.build_page_docid_mapping(path, mappingFileName)
    builder = SimpleIndexBuilder()
    builder.init(mappingFileName, '../common/StopWordsList.txt')
    builder.build_index(path, indexFileName)
    
    reader = SimpleIndexReader()
    index = reader.read(indexFileName)
    readableFileName = '../index_chunk/readableIndex'
    with open(readableFileName, 'w') as f:
        for (k, v) in index.get_indexmap().items():
            f.write(str(k) + '\n' + str(v) + '\n')
