#!/usr/bin/python

import os
import shutil

from UrlDumper import UrlDumper
from UrlDumper import USE_LEVELDB

if __name__ == '__main__':
    if USE_LEVELDB == True:
        UrlDumper.Init('.', 'urlPages')
    else:
        os.mkdir('./test')
        UrlDumper.Init('./test', None)

    url1 = 'http://www.test1.com'
    page1 = 'this is test page1'
    UrlDumper.Write(url1, page1)
    url2 = 'http://www.test2.com'
    page2 = 'this is test page2'
    UrlDumper.Write(url2, page2)
    url3 = 'http://www.test3.com'
    page3 = 'this is test page3'
    UrlDumper.Write(url3, page3)

    assert UrlDumper.Read(url1) == page1
    assert UrlDumper.Read(url2) == page2
    assert UrlDumper.Read(url3) == page3

    if USE_LEVELDB == True:
        pass
        #print 'remove ./urlPages'
        #shutil.rmtree('./urlPages')
    else:
        shutil.rmtree('./test')
