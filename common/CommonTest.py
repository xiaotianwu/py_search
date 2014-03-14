#!/usr/bin/python

import os
import unittest
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
  
class CommonTest(unittest.TestCase):
    def setUp(self):
        os.system('mkdir -p path1/path2/path3')
        os.system('touch path1/file1')
        os.system('touch path1/path2/file2')
        os.system('touch path1/path2/path3/file3')
        os.system('mkdir emptypath')

    def tearDown(self):
        os.system('rm path1 -r')
        os.system('rm emptypath -r')

    def testPadding(self):
        self.assertEqual(LeftPadding('abc', 5), '  abc')
        self.assertEqual(LeftPadding('abc', 3), 'abc')
        self.assertEqual(RightPadding('abc', 5), 'abc  ')
        self.assertEqual(RightPadding('abc', 3), 'abc')
    
    def testDirHandler(self):
        files = DirHandler.GetAllFiles('./empthpath', recursive = True)
        self.assertEqual(len(set(files)), 0)
        files = DirHandler.GetAllFiles('./empthpath', recursive = False)
        self.assertEqual(len(set(files)), 0)
        files = DirHandler.GetAllFiles('./path1', recursive = True)
        self.assertEqual(set(files), set(['./path1/file1',
                                          './path1/path2/file2',
                                          './path1/path2/path3/file3']))
        files = DirHandler.GetAllFiles('./path1', recursive = False)
        self.assertEqual(set(files), set(['./path1/file1']))

    def testConverter(self):
        url = 'http://www.facebook.com'
        fileName = 'http:^^www.facebook.com'
        self.assertEqual(Converter.UrlToFileName(url), fileName)
        self.assertEqual(Converter.FileNameToUrl(fileName), url)
        self.assertEqual(Converter.FileNameToUrl('/usr/bin/' + fileName), url)

    def testAsync(self):
        InitThreadPool()
        TestAsync1()
        TestAsync2(2, set([1, 2, 3]), callback = TestCallBack)
        time.sleep(4)
        UninitThreadPool()

if __name__ == '__main__':
    unittest.main()
