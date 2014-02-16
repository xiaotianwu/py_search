#!/usr/bin/python

import os
import shutil

from IntermediateGenerator import IntermediateGenerator

path = './testdir/'
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)
testfile1 = path + 'a.html'
testfile2 = path + 'b.html'
os.mknod(testfile1)
os.mknod(testfile2)

IntermediateGenerator.build_page_docid_mapping(path, 'testMapping', False)
mapping = IntermediateGenerator.read_page_docid_mapping('testMapping')
assert 'a.html' in mapping
assert 'b.html' in mapping

os.remove('testMapping')
shutil.rmtree(path)
