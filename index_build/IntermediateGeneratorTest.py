#!/usr/bin/python

from IntermediateGenerator import IntermediateGenerator
import os

path = '../page_chunk/'
IntermediateGenerator.build_page_docid_mapping(path, 'testMapping', False)
mapping = IntermediateGenerator.read_page_docid_mapping('testMapping')
print mapping
os.remove('testMapping')
