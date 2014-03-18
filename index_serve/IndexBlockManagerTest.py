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
        self.assertEqual(block.termidStart, 0)
        self.assertEqual(block.termidEnd, 1)
        self.assertEqual(block.mappingFile, 'a')
        self.assertEqual(block.type, 'b')
        block = manager.GetBlock(3)
        self.assertEqual(block.termidStart, 2)
        self.assertEqual(block.termidEnd, 5)
        self.assertEqual(block.mappingFile, 'c')
        self.assertEqual(block.type, 'd')
        block = manager.GetBlock(10)
        self.assertEqual(block.termidStart, 6)
        self.assertEqual(block.termidEnd, 10)
        self.assertEqual(block.mappingFile, 'e')
        self.assertEqual(block.type, 'f')
        block = manager.GetBlock(11)
        self.assertEqual(block, None)  

    def testGetAllBlocks(self):
        mappingStr = '0,1:a:b;2,5:c:d;6,10:e:f'
        manager = IndexBlockManager('', mappingStr)
        blocks = manager.GetAllBlocks()
        blocksClone = [IndexBlock(0, 1, 'a', 'b')]
        blocksClone.append(IndexBlock(2, 5, 'c', 'd'))
        blocksClone.append(IndexBlock(6, 10, 'e', 'f'))
        self.assertListEqual(blocks, blocksClone)

if __name__ == '__main__':
    unittest.main()

