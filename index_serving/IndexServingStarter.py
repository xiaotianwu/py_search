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

from IndexServingImpl import IndexServingHandler
import IndexServing

handler = IndexServingHandler()
processor = IndexServing.Processor(handler)
transport = TSocket.TServerSocket()
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print "Start Server..."
server.serve()
print "Done"
