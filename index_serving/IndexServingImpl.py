import sys
sys.path.append('thrift/gen-py/index_serving')
sys.path.append('../common')

import IndexServing
from ttypes import IndexServingStatus
from ttypes import IndexServingProperty

class IndexServingHandler(IndexServing.Iface):
    def Ping(self):
        print "incoming ping"
        return IndexServingProperty()

    def Search(self, termIds):
        pass
