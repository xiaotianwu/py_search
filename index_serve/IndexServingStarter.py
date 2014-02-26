#!/usr/bin/python

from IndexServingImpl import IndexServing

if __name__ == '__main__':
    server = IndexServing()
    server.init('../index_chunk/testIndex')
    server.start()
