from IndexConfig import IndexMergerFatcory

class IndexMerger:
    def __init__(self):
        self._indexToMerge = []
        self._merger = IndexMergerFatcory.Get()

    def Add(self, index):
        self._merger.Add(index)

    def DoMerge(self):
        return self._merger.DoMerge()
