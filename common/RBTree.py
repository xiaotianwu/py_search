RED = True
BLACK = False

class RBTreeNode:
    __slots__ = ['key', 'val', 'color', 'left', 'right', 'parent']
    
    def __init__(self, key, val = None):
        self.key = key
        self.val = val
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    '''key is unique'''
    def __init__(self, root):
        self._root = root

    def root(self):
        return self._root

    def Insert(self, key, val):
        newNode = RBTreeNode(key, val)
        insertPos = self._SearchInsertPos(self._root, None, key)
        if insertPos.key > key:
            assert insertPos.left == None
            insertPos.left = newNode
            newNode.parent = insertPos
        else:
            assert insertPos.right == None
            insertPos.right = newNode
            newNode.parent = insertPos
        self._InsertFix(newNode)
        
    def Search(self, key):
        return self._Search(node, key)

    def _InsertFix(self, node):
        while True:
            if node == self._root:
                node.color = BLACK
                break
            parent = node.parent
            if parent.color == BLACK:
                break
            grandParent = parent.parent
            assert grandParent != None
            if grandParent.left == parent:
                uncle = grandParent.right
            else:
                uncle = grandParent.left
            if uncle == None or uncle.color == BLACK:
                if node == parent.right:
                    self._LeftRotate(parent)
                else:
                    parent.color = BLACK
                    grandParent.color = RED
                    if grandParent.left == parent:
                        self._RightRotate(grandParent)
                    else:
                        self._LeftRotate(grandParent)
                node = parent
            elif uncle.color == RED:
                parent.color = BLACK
                uncle.color = BLACK
                grandParent.color = RED
                node = grandParent
            else:
                raise Exception('RBTree corrupt')

    def CheckIsLegal(self):
        if self._root.color != BLACK:
            return False
        blackNodeNum, retCode = self._CheckIsLegal(self._root)
        return retCode

    def _CheckIsLegal(self, node):
        if node == None:
            return 1, True
        if node.left != None:         
            leftBlackNodeNum, retCode = self._CheckIsLegal(node.left)
            if retCode == False:
                return -1, False
        if node.right != None:
            rightBlackNodeNum, retCode = self._CheckIsLegal(node.right)
            if retCode == False:
                return -1, False
        if leftBlackNodeNum == rightBlackNodeNum:
            return rightBlackNodeNum, True
        else
            return -1, False

    def _LeftRotate(self, node):
        assert node.right != None
        if node == self._root:
            self._root = node.right
        rightChild = node.right
        parent = node.parent
        if parent != None:
            if parent.left == node:
                parent.left = rightChild
            else:
                parent.right = rightChild
        rightChild.parent = parent
        node.right = rightChild.left
        if rightChild.left != None:
            rightChild.left.parent = node
        rightChild.left = node
        node.parent = rightChild

    def _RightRotate(self, node):
        assert node.left != None
        if node == self._root:
            self._root = node.left
        leftChild = node.left
        parent = node.parent
        if parent != None:
            if parent.left == node:
                parent.left = leftChild
            else:
                parent.right = leftChild
        leftChild.parent = parent
        node.right = leftChild.right
        if leftChild.right != None:
            leftChild.right.parent = node
        leftChild.right = node
        node.parent = leftChild

    def _Search(self, node, key):
        if node == None:
            return None
        elif node.key == key:
            return node.val
        elif node.key > key:
            return _Search(node.left, key)
        elif node.key < key:
            return _Search(node.right, key)
       
    def _SearchInsertPos(self, node, parentNode, key):
        if node == None:
            return parentNode
        elif node.key > key:
            return _SearchInsertPos(node.left, node, key)
        elif node.key < key:
            return _SearchInsertPos(node.right, node, key)

    def Delete(self, key):
        pass

    def _Delete(self, key):
        pass

    def _DeleteFix(self, key):
        pass
