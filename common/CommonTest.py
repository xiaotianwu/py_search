#!/usr/bin/python

import os
import time

from Common import *
from Common import UrlFileNameConverter as Converter

@CallBack
def TestCallBack():
    print('test callback')

@Async
def TestAsync1():
    print('test func 1')
    time.sleep(2)
    print('test func 1 again')

@Async
def TestAsync2(i, s, callback):
    print('test func 2', i)
    print('set is', s)
    print('callback_func is', callback)
    callback()
  
def CreateTestData():
    os.system('mkdir -p path1/path2/path3')
    os.system('touch path1/file1')
    os.system('touch path1/path2/file2')
    os.system('touch path1/path2/path3/file3')
    os.system('mkdir emptypath')
    
def DeleteTestData():
    os.system('rm path1 -r')
    os.system('rm emptypath -r')

if __name__ == '__main__':
    assert LeftPadding('abc', 5) == '  abc'
    assert LeftPadding('abc', 3) == 'abc'
    assert RightPadding('abc', 5) == 'abc  '
    assert RightPadding('abc', 3) == 'abc'

    CreateTestData()

    files = DirHandler.GetAllFiles('./empthpath', recursive = True)
    assert len(set(files)) == 0
    files = DirHandler.GetAllFiles('./empthpath', recursive = False)
    assert len(set(files)) == 0
    files = DirHandler.GetAllFiles('./path1', recursive = True)
    assert set(files) == set(['./path1/file1',
                              './path1/path2/file2',
                              './path1/path2/path3/file3'])
    files = DirHandler.GetAllFiles('./path1', recursive = False)
    assert set(files) == set(['./path1/file1'])
    
    url = 'http://www.facebook.com'
    fileName = 'http:^^www.facebook.com'
    assert Converter.UrlToFileName(url) == fileName
    assert Converter.FileNameToUrl(fileName) == url
    assert Converter.FileNameToUrl('/usr/bin/' + fileName) == url

    InitThreadPool()
    TestAsync1()
    TestAsync2(2, set([1, 2, 3]), callback = TestCallBack)
    time.sleep(4)
    UninitThreadPool()

    DeleteTestData()
