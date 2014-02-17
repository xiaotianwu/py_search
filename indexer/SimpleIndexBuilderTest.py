#!/usr/bin/python
import sys
import os
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from IntermediateGenerator import IntermediateGenerator as InGen
from SimpleIndexBuilder import SimpleIndexBuilder
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader

if __name__ == '__main__':
    path = '../page_chunk/'
    mappingFileName = '../index_chunk/testMapping'
    indexFileName = '../index_chunk/testIndex'
    readableFileName = '../index_chunk/readableIndex'
    
    InGen.build_page_docid_mapping(path, mappingFileName, False)
    builder = SimpleIndexBuilder(True)
    builder.init(mappingFileName, '../common/StopWordsList.txt')
    builder.build_index(path, indexFileName)
    
    reader = SimpleIndexReader()
    index = reader.read(indexFileName)
    f = open(readableFileName, 'w')
    for (k, v) in index.get_indexmap().items():
        f.write(str(k) + '\n' + str(v) + '\n')
    f.close()
