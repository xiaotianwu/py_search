#!/usr/bin/python
import sys
import os
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from IntermediateGenerator import IntermediateGenerator
from SimpleIndexBuilder import SimpleIndexBuilder
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader

path = '../page_chunk/'
IntermediateGenerator.build_page_docid_mapping(path, 'testMapping', False)

builder = SimpleIndexBuilder()
builder.init('testMapping', '../common/StopWordsList.txt')
builder.build_index('../page_chunk/', 'testIndex')

reader = SimpleIndexReader()
index = reader.read('testIndex')
f = open('IndexReadableFile', 'w')
for (k, v) in index.get_indexmap().items():
    f.write(str(k) + '\n' + str(v) + '\n')
f.close()

os.remove('testMapping')
os.remove('testIndex')
