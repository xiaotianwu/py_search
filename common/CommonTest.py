#!/usr/bin/python

import time

from Common import async
from Common import call_back
from Common import DirHandler
from Common import UrlFileNameConverter

@call_back
def test_callback():
    print 'test callback'

@async
def test_async1():
    print 'test func 1'
    time.sleep(2)
    print 'test func 1 again'

@async
def test_async2(i, callback):
    print 'test func 2', i
    print 'callback_func is', callback
    callback()
  
    
if __name__ == '__main__':
    print DirHandler.get_all_files('.', recursive = False)
    print DirHandler.get_all_files('.', recursive = True)
    
    print UrlFileNameConverter.url_to_filename('http://www.facebook.com')
    print UrlFileNameConverter.filename_to_url('http:^^facebook.com')
    print UrlFileNameConverter.filename_to_url('/usr/bin/http:^^facebook.com')

    test_async1()
    test_async2(2, callback = test_callback)
    time.sleep(4)
