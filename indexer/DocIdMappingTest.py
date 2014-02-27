#!/usr/bin/python

import os
import shutil

from DocIdMapping import DocIdMappingHandler as Handler

if __name__ == '__main__':
    path = './testdir/'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    testfile1 = path + 'a.html'
    testfile2 = path + 'b.html'
    os.mknod(testfile1)
    os.mknod(testfile2)
    
    Handler.build_docid_mapping(path, 'testMapping')
    mapping = Handler.read_docid_mapping('testMapping')
    assert 'a.html' in mapping
    assert 'b.html' in mapping
    
    print(mapping)
    os.remove('testMapping')
    shutil.rmtree(path)
