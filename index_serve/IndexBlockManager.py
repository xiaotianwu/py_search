from IndexConfig import INDEXFOLDER
from IndexConfig import INDEXMAPPING

class IndexBlock:
    def __init__(self, docidStart, docidEnd, mappingFile, blockType):
        self._docidStart = docidStart
        self._docidEnd = docidEnd
        self._mappingFile = mappingFile
        self._blockType = blockType

class IndexBlockManager:
    def __init__(self):
        self._indexFolder = INDEXFOLDER
        self._indexMappingRawStr = INDEXMAPPING
        self._ParseIndexMappingStr(INDEXMAPPING)

    def _ParseIndexMappingStr(rawStr):
        allMapping = rawStr.strip().split(';')
        for mapping in allMapping:
            mapping = mapping.split(':')
            assert len(mapping) >= 3
            docidRange = mapping[0][1:-2].split(',')
            block = IndexBlock(int(docidRange[0]),
                               int(docidRange[1]),
                               mapping[1], mapping[2])
