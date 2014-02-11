import sys
sys.path.append('thrift/gen-py/index_serving')
sys.path.append('../common')

import IndexServing
from ttypes import IndexServingStatus
from ttypes import IndexServingProperty

class IndexServingHandler(IndexServing.Iface):
    def ping(self):
        print "incoming ping"
        return IndexServingProperty()

    def search(self, termIds):
        pass
