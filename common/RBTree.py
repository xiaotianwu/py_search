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
    def __init__(self, root = None):
        self._root = root

    def root(self):
        return self._root

    def Insert(self, key, val):
        global BLACK, RED
        newNode = RBTreeNode(key, val)
        if self._root == None: 
            self._root = newNode
            self._root.color = BLACK
            return
        insertPos = self._SearchInsertPos(self._root, None, key)
        if insertPos.key > key:
            assert insertPos.left == None
            insertPos.left = newNode
            newNode.parent = insertPos
        elif insertPos.key < key:
            assert insertPos.right == None
            insertPos.right = newNode
            newNode.parent = insertPos
        else:
            raise Exception('key exist' + str(key))
        self._InsertFix(newNode)
        
    def Find(self, key):
        cur = self._root
        while cur != None:
            if cur.key == key:
              return cur.val
            elif cur.key > key:
              cur = cur.left
            else:
              cur = cur.right
        return None
 
    def LowerBound(self, key):
        '''return kv pair'''
        cur = self._root
        lowerBound = None
        while cur != None:
            if cur.key == key:
              return cur.key, cur.val
            elif cur.key > key:
              cur = cur.left
            else:
              lowerBound = cur
              cur = cur.right
        if lowerBound == None:
            return None, None
        else:
            return lowerBound.key, lowerBound.val

    def _InsertFix(self, node):
        global BLACK, RED
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
                    node = parent
                else:
                    parent.color = BLACK
                    grandParent.color = RED
                    if grandParent.left == parent:
                        self._RightRotate(grandParent)
                    else:
                        self._LeftRotate(grandParent)
            elif uncle.color == RED:
                parent.color = BLACK
                uncle.color = BLACK
                grandParent.color = RED
                node = grandParent
            else:
                raise Exception('RBTree corrupt')

    def CheckLegality(self):
        global BLACK, RED
        if self._root.color != BLACK:
            return False
        blackNodeNum, retCode = self._CheckRBTreeProperty(self._root)
        if retCode == False:
            return False
                    
        inorderArray = list()
        self.InOrderTraverseKey(self._root, inorderArray)
        if self._CheckIsMonoArray(inorderArray) == True:
            return True
        else:
            return False

    def InOrderTraverseKey(self, node, array):
        if node.left != None:
            self.InOrderTraverseKey(node.left, array)
        array.append(node.key)
        if node.right != None:
            self.InOrderTraverseKey(node.right, array)

    def InOrderTraverseValue(self, node, array):
        if node.left != None:
            self.InOrderTraverseValue(node.left, array)
        array.append(node.val)
        if node.right != None:
            self.InOrderTraverseValue(node.right, array)

    def _CheckIsMonoArray(self, array):
        last = 0 - 2 << 64
        for item in array:
            if item >= last:
                last = item
            else:
                return False
        return True

    def _CheckRBTreeProperty(self, node):
        global BLACK, RED
        if node == None:
            return 1, True
        if node.color == RED:
            if node.left != None and node.left.color == RED:
                return -1, False
            if node.right != None and node.right.color == RED:
                return -1, False
        leftBlackNodeNum, retCode = self._CheckRBTreeProperty(node.left)
        if retCode == False:
            return -1, False
        rightBlackNodeNum, retCode = self._CheckRBTreeProperty(node.right)
        if retCode == False:
            return -1, False
        if leftBlackNodeNum == rightBlackNodeNum:
            blackNodeNum = leftBlackNodeNum + 1 if node.color == BLACK\
                                                else leftBlackNodeNum
            return blackNodeNum, True
        else:
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
        node.left = leftChild.right
        if leftChild.right != None:
            leftChild.right.parent = node
        leftChild.right = node
        node.parent = leftChild

    def _SearchInsertPos(self, node, parentNode, key):
        if node == None:
            return parentNode
        elif node.key > key:
            return self._SearchInsertPos(node.left, node, key)
        elif node.key < key:
            return self._SearchInsertPos(node.right, node, key)

    def Delete(self, key):
        pass

    def _Delete(self, key):
        pass

    def _DeleteFix(self, key):
        pass
