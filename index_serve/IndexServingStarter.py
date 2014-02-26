#!/usr/bin/python

from IndexServingImpl import IndexServing

if __name__ == '__main__':
    #server = IndexServing(blocking = True)
    #server = IndexServing(blocking = False)
    server = IndexServing(blocking = True, threaded = True)
    server.init('../index_chunk/testIndex',
                True,
                '../index_chunk/testTermidMapping')
    server.start()
