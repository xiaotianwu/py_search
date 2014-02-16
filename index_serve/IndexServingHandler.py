import sys
sys.path.append('thrift/gen-py/index_serving')
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

import IndexServing
from ttypes import IndexServingStatus
from ttypes import IndexServingProperty
from SimpleIndex import *

class IndexServingHandler(IndexServing.Iface):
    def init(self, simpleIndex):
        if not isinstance(simpleIndex, SimpleIndex):
            print 'SimpleIndex type error', type(simpleIndex)
        self.__indexHandler = SimpleIndexHandler(simpleIndex)
        
    def ping(self):
        print "incoming ping"
        return IndexServingProperty()

    def search(self, terms):
        pass
