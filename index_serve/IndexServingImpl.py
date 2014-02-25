#!/usr/bin/env python

import sys
sys.path.append('thrift/gen-py/index_serving')

from thrift.protocol import TBinaryProtocol
from thrift.server import TNonblockingServer
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.transport import TTwisted
from twisted.internet import reactor

from IndexServingHandler import IndexServingHandler
from SimpleIndex import *
import IndexServing

class IndexServing:
    def __init__(self, port = 1234, blocking = True, threaded = False):
        self.__port = port

    def init(self, indexFileName):
        reader = SimpleIndexReader()
        self.__index = reader.read(indexFileName)

    def start(self):
        print "Start Server..."
        if blocking == True:
            handler = IndexServingHandler(self.__index)
            processor = IndexServing.Processor(handler)
            transport = TSocket.TServerSocket()
            tfactory = TTransport.TBufferedTransportFactory()
            pfactory = TBinaryProtocol.TBinaryProtocolFactory()
            if threaded == True:
                self.__server = TServer.TSimpleServer(
                                    processor, transport, tfactory, pfactory)
            else:
                self.__server = TServer.TThreadedServer(
                                    processor, transport, tfactory, pfactory)
            self.__server.serve()
        else:
            reactor.listenTCP(11000,
                TTwisted.ThriftServerFactory(
                    processor = processor,
                    iprot_factory = TBinaryProtocol.TBinaryProtocolFactory()))

            self.__reactor = reactor
            self.__reactor.run()

        print "Done"
