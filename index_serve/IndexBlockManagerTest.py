import unittest

from IndexBlockManager import *

class IndexBlockManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testParsingMappingStr(self):
        mappingStr = '0,1:a:b;2,5:c:d;6,10:e:f'
        manager = IndexBlockManager('', mappingStr)
        self.assertEqual(manager.GetBlock(-1), None)
        block = manager.GetBlock(0)
        block2 = manager.GetBlock(1)
        self.assertEqual(block, block2)
        self.assertEqual(block.docidStart, 0)
        self.assertEqual(block.docidEnd, 1)
        self.assertEqual(block.mappingFile, 'a')
        self.assertEqual(block.blockType, 'b')
        block = manager.GetBlock(3)
        self.assertEqual(block.docidStart, 2)
        self.assertEqual(block.docidEnd, 5)
        self.assertEqual(block.mappingFile, 'c')
        self.assertEqual(block.blockType, 'd')
        block = manager.GetBlock(10)
        self.assertEqual(block.docidStart, 6)
        self.assertEqual(block.docidEnd, 10)
        self.assertEqual(block.mappingFile, 'e')
        self.assertEqual(block.blockType, 'f')
        block = manager.GetBlock(11)
        self.assertEqual(block, None)  

if __name__ == '__main__':
    unittest.main()

