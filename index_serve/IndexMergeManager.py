class IndexMergeManager:
    def __init__(self, merger):
        self._indexToMerge = []
        self._merger = merger

    def Add(self, index):
        self._merger.Add(index)

    def DoMerge(self):
        return self._merger.DoMerge()
