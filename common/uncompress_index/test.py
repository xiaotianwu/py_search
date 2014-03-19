#!/usr/bin/python

from ctypes import *

class TestStruct(Structure):
    _fields_ = [('data', POINTER(c_uint)),
                ('len', c_uint)]

if __name__ == '__main__':
    mylib = CDLL('/root/py_search/common/uncompress_index/test.so')
    print mylib
    ts = TestStruct()
    pts = pointer(ts)
    mylib.TestFunc(pts)
    for i in range(0, ts.len):
        print ts.data[i]
