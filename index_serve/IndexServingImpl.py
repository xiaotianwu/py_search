#!/usr/bin/env python

import sys
sys.path.append('thrift/gen-py/index_serving')
sys.path.append('../indexer/')

from thrift.protocol import TBinaryProtocol
from thrift.server import TNonblockingServer
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.transport import TTwisted
from twisted.internet import reactor

from IndexServingHandler import IndexServingHandler
from SimpleIndex import *
from IndexServing import Processor as IndexServingProcessor
from TermIdMapping import TermIdMappingHandler as TermMapHandler

class IndexServing:
    def __init__(self, port = 1234, blocking = True, threaded = False):
        self._port = port
        self._blocking = blocking
        self._threaded = threaded
        self._debugServerMode = False

    def init(self, indexFileName,
             debugServerMode = False, termidMappingFile = None):
        reader = SimpleIndexReader()
        self._index = reader.read(indexFileName)
        assert isinstance(self._index, SimpleIndex) == True
        self._debugServerMode = debugServerMode
        if self._debugServerMode == True:
            self._termidMapping = TermMapHandler.read_termid_mapping(
                                      termidMappingFile)

    def start(self):
        print "Start Server..."
        if self._blocking == True:
            handler = IndexServingHandler(self._index)
            if self._debugServerMode == True:
                handler.load_debug_mapping(self._termidMapping)
            processor = IndexServingProcessor(handler)
            transport = TSocket.TServerSocket()
            tfactory = TTransport.TBufferedTransportFactory()
            pfactory = TBinaryProtocol.TBinaryProtocolFactory()
            if self._threaded == False:
                self._server = TServer.TSimpleServer(
                                    processor, transport, tfactory, pfactory)
            else:
                self._server = TServer.TThreadedServer(
                                    processor, transport, tfactory, pfactory)
            self._server.serve()
        else:
            reactor.listenTCP(
                self._port,
                TTwisted.ThriftServerFactory(
                    processor = processor,
                    iprot_factory = TBinaryProtocol.TBinaryProtocolFactory()))

            self._reactor = reactor
            self._reactor.run()

        print "Done"
