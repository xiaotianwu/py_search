#!/usr/bin/python

import leveldb

if __name__ == '__main__':
    db = leveldb.LevelDB('url_and_page')
    iterator = db.RangeIter()
    size = 0
    while True:
       try:
           print iterator.next()[0]
           size += 1
       except StopIteration:
           break
    print 'size =', size
