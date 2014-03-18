from common.RBTree import RBTree

class IndexBlock:
    __slots__ = ['termidStart', 'termidEnd', 'mappingFile', 'type']

    def __init__(self, termidStart, termidEnd, mappingFile, blockType):
        self.termidStart = termidStart
        self.termidEnd = termidEnd
        self.mappingFile = mappingFile
        self.type = blockType

    def __eq__(self, indexBlock):
        if indexBlock == None:
            return False
        if self.termidStart == indexBlock.termidStart and\
           self.termidEnd == indexBlock.termidEnd and\
           self.mappingFile == indexBlock.mappingFile and\
           self.type == indexBlock.type:
            return True
        return False

class IndexBlockManager:
    def __init__(self, folder, mappingStr):
        self._indexFolder = folder
        self._indexMappingRawStr = mappingStr
        self._blockTree = RBTree()
        self._ParseIndexMappingStr()

    def _ParseIndexMappingStr(self):
        rawStr = self._indexMappingRawStr
        allMapping = rawStr.strip().split(';')
        for mapping in allMapping:
            mapping = mapping.split(':')
            assert len(mapping) >= 3
            docidRange = mapping[0].split(',')
            key = int(docidRange[0])
            block = IndexBlock(key,
                               int(docidRange[1]),
                               mapping[1], mapping[2])
            self._blockTree.Insert(key, block)

    def GetBlock(self, termId):
        key, block = self._blockTree.LowerBound(termId)
        if block == None:
            return None
        if termId >= block.termidStart and termId <= block.termidEnd:
            return block
        else:
            return None

    def GetAllBlocks(self):
        blocks = []
        self._blockTree.InOrderTraverseValue(self._blockTree.root(), blocks)
        return blocks
