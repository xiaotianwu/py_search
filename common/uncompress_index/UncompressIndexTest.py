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

    def testTrivialIntersection(self):
        pl1 = PostingList()
        pl1.len = 2
        DSArrayType = DocScorePair * pl1.len
        dsArray = DSArrayType()
        dsArray[0] = DocScorePair(0)
        dsArray[1] = DocScorePair(2)
        pl1.list = dsArray
        pl2 = PostingList()
        pl2.len = 2
        dsArray2 = DSArrayType()
        dsArray2[0] = DocScorePair(1)
        dsArray2[1] = DocScorePair(2)
        pl2.list = dsArray2
        handler = UncompressIndexHandler()
        handler.Add(pl1)
        handler.Add(pl2)
        dSet = handler.Intersect()
        self.assertEqual(dSet.docids[0], 2)

if __name__ == '__main__':
    unittest.main()
