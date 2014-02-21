#!/usr/bin/env python

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from thrift.server import TNonblockingServer
from twisted.internet import reactor
from thrift.transport import TTwisted

import sys
sys.path.append('thrift/gen-py/index_serving')

from IndexServingHandler import IndexServingHandler
import IndexServing

class IndexServing:
    __handler = IndexServingHandler()
    __processor = IndexServing.Processor(handler)
    __transport = TSocket.TServerSocket()
    __tfactory = TTransport.TBufferedTransportFactory()
    __pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    def __init__(self, port = 1234):
        self.__port = port
        pass

    def start(self):
        self.__server = TServer.TSimpleServer(self.__processor, self.__transport, self.__tfactory, self.__pfactory)
        print "Start Server..."
        self.__server.serve()
        print "Done"
        
