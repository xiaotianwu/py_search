#!/usr/bin/python
import unittest

from UncompressIndex import *

class UncompressIndexTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCStructsReadWrite(self):
        pl = PostingList()
        pl.len = 1000
        DSArrayType = DocScorePair * pl.len
        dsArray = DSArrayType()
        for i in range(0, pl.len):
            dsPair = DocScorePair(i)
            dsArray[i] = dsPair
        pl.list = dsArray
        for i in range(0, pl.len):
            self.assertEqual(pl.list[i].docid, i)

    def testCLibFunc(self):
        dSet = DocidSet()
        dSet.len = 10
        DSetArrayType = c_uint * dSet.len
        dSet.docids = DSetArrayType()
        for i in range(0, dSet.len):
            dSet.docids[i] = i
        uncompressIndexLib.PrintDocidSet(dSet)

if __name__ == '__main__':
    unittest.main()
