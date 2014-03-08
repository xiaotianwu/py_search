#!/usr/bin/python

import os
import time

from Common import *
from Common import UrlFileNameConverter as Converter

@call_back
def test_callback():
    print('test callback')

@async
def test_async1():
    print('test func 1')
    time.sleep(2)
    print('test func 1 again')

@async
def test_async2(i, s, callback):
    print('test func 2', i)
    print('set is', s)
    print('callback_func is', callback)
    callback()
  
def create_testdata():
    os.system('mkdir -p path1/path2/path3')
    os.system('touch path1/file1')
    os.system('touch path1/path2/file2')
    os.system('touch path1/path2/path3/file3')
    os.system('mkdir emptypath')
    
def delete_testdata():
    os.system('rm path1 -r')
    os.system('rm emptypath -r')

if __name__ == '__main__':
    assert left_padding('abc', 5) == '  abc'
    assert left_padding('abc', 3) == 'abc'
    assert right_padding('abc', 5) == 'abc  '
    assert right_padding('abc', 3) == 'abc'

    create_testdata()

    files = DirHandler.get_all_files('./empthpath', recursive = True)
    assert len(set(files)) == 0
    files = DirHandler.get_all_files('./empthpath', recursive = False)
    assert len(set(files)) == 0
    files = DirHandler.get_all_files('./path1', recursive = True)
    assert set(files) == set(['./path1/file1',
                              './path1/path2/file2',
                              './path1/path2/path3/file3'])
    files = DirHandler.get_all_files('./path1', recursive = False)
    assert set(files) == set(['./path1/file1'])
    
    url = 'http://www.facebook.com'
    fileName = 'http:^^www.facebook.com'
    assert Converter.url_to_filename(url) == fileName
    assert Converter.filename_to_url(fileName) == url
    assert Converter.filename_to_url('/usr/bin/' + fileName) == url

    InitThreadPool()
    test_async1()
    test_async2(2, set([1, 2, 3]), callback = test_callback)
    time.sleep(4)
    UninitThreadPool()

    delete_testdata()
