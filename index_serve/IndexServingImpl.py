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
    def __init__(self, port = 9090, blocking = True, threaded = False):
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
        handler = IndexServingHandler(self._index)
        if self._debugServerMode == True:
            handler.load_debug_mapping(self._termidMapping)
        processor = IndexServingProcessor(handler)
        transport = TSocket.TServerSocket(port = self._port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        if self._blocking == True:
            if self._threaded == False:
                print 'Start blocking non-threaded server...'
                self._server = TServer.TSimpleServer(
                                    processor, transport, tfactory, pfactory)
            else:
                print 'Start blocking threaded server...'
                self._server = TServer.TThreadedServer(
                                    processor, transport, tfactory, pfactory)
            self._server.serve()
        else:
            print 'Start non-blocking server...'
            reactor.listenTCP(
                self._port,
                TTwisted.ThriftServerFactory(
                    processor = processor, iprot_factory = pfactory))
            reactor.run()

        print "Done"
