#!/usr/bin/python

from multiprocessing import Pool
import time

from Common import *

@call_back
def test_callback():
    print 'test callback'

@async
def test_async1():
    print 'test func 1'
    time.sleep(2)
    print 'test func 1 again'

@async
def test_async2(i, s, callback):
    print 'test func 2', i
    print 'set is', s
    print 'callback_func is', callback
    callback()
  
    
if __name__ == '__main__':
    print DirHandler.get_all_files('.', recursive = False)
    print DirHandler.get_all_files('.', recursive = True)
    
    print UrlFileNameConverter.url_to_filename('http://www.facebook.com')
    print UrlFileNameConverter.filename_to_url('http:^^facebook.com')
    print UrlFileNameConverter.filename_to_url('/usr/bin/http:^^facebook.com')

    InitThreadPool()

    test_async1()
    test_async2(2, set([1, 2, 3]), callback = test_callback)
    time.sleep(4)

    UninitThreadPool()
