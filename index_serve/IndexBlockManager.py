from common.RBTree import RBTree

class IndexBlock:
    def __init__(self, docidStart, docidEnd, mappingFile, blockType):
        self.docidStart = docidStart
        self.docidEnd = docidEnd
        self.mappingFile = mappingFile
        self.blockType = blockType

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
        if termId >= block.docidStart and termId <= block.docidEnd:
            return block
        else:
            return None

    def GetAllBlocks(self):
        raise Exception('need implement')
