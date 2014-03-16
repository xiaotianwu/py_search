#!/usr/bin/python

import pdb
import unittest

from RBTree import *

class RBTreeTest(unittest.TestCase):
    def testRotation(self):
        root = RBTreeNode(4)
        root.right = RBTreeNode(6)
        root.right.parent = root
        tree = RBTree(root)
        tree._LeftRotate(tree.root())
        self.assertEqual(tree.root().key, 6)
        self.assertEqual(tree.root().parent, None)
        self.assertEqual(tree.root().right, None)
        self.assertEqual(tree.root().left.key, 4)
        self.assertEqual(tree.root().left.parent.key, 6)
        self.assertEqual(tree.root().left.left, None)
        self.assertEqual(tree.root().left.right, None)

        root = RBTreeNode(4)
        root.right = RBTreeNode(6)
        root.right.parent = root
        root.right.left = RBTreeNode(5)
        root.right.left.parent = root.right
        root.right.right = RBTreeNode(7)
        root.right.right.parent = root.right
        tree = RBTree(root)
        tree._LeftRotate(tree.root())
        self.assertEqual(tree.root().key, 6)
        self.assertEqual(tree.root().left.key, 4)
        self.assertEqual(tree.root().left.parent.key, 6)
        self.assertEqual(tree.root().left.left, None)
        self.assertEqual(tree.root().left.right.key, 5)
        self.assertEqual(tree.root().left.right.parent.key, 4)
        self.assertEqual(tree.root().left.right.left, None)
        self.assertEqual(tree.root().left.right.right, None)
        self.assertEqual(tree.root().right.key, 7)
        self.assertEqual(tree.root().right.parent.key, 6)
        self.assertEqual(tree.root().right.left, None)
        self.assertEqual(tree.root().right.right, None)

        root = RBTreeNode(4)
        root.right = RBTreeNode(6)
        root.right.parent = root
        root.right.left = RBTreeNode(5)
        root.right.left.parent = root.right
        root.right.right = RBTreeNode(8)
        root.right.right.parent = root.right
        root.right.right.left = RBTreeNode(7)
        root.right.right.left.parent = root.right.right
        root.right.right.right = RBTreeNode(9)
        root.right.right.right.parent = root.right.right
        tree = RBTree(root)
        tree._LeftRotate(root.right)
        self.assertEqual(tree.root().key, 4)
        self.assertEqual(tree.root().left, None)
        self.assertEqual(tree.root().right.key, 8)
        self.assertEqual(tree.root().right.parent.key, 4)
        self.assertEqual(tree.root().right.left.key, 6)
        self.assertEqual(tree.root().right.left.left.key, 5)
        self.assertEqual(tree.root().right.left.left.left, None)
        self.assertEqual(tree.root().right.left.left.right, None)
        self.assertEqual(tree.root().right.left.right.key, 7)
        self.assertEqual(tree.root().right.left.right.left, None)
        self.assertEqual(tree.root().right.left.right.right, None)
        self.assertEqual(tree.root().right.right.key, 9)
        self.assertEqual(tree.root().right.right.left, None)
        self.assertEqual(tree.root().right.right.right, None)

    def testInsertTinySet(self):
        tree = RBTree()
        tree.Insert(1, None)
        self.assertTrue(tree.CheckLegality())
        tree.Insert(2, None)
        self.assertTrue(tree.CheckLegality())
        tree.Insert(3, None)
        pdb.set_trace()
        self.assertTrue(tree.CheckLegality())
        tree.Insert(4, None)
        self.assertTrue(tree.CheckLegality())
        tree.Insert(5, None)
        self.assertTrue(tree.CheckLegality())

if __name__ == '__main__':
    unittest.main()
