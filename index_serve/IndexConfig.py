#!/usr/bin/python

import os
import ConfigParser

from common.Logger import Logger
from common.uncompress_index.UncompressIndex import *

configParserLogger = Logger.Get('IndexConfig')

configFile = os.environ['PY_SEARCH_ROOT'] + '/config/IndexServe.conf'
configParserLogger.info('read config file: ' + configFile)
configParser = ConfigParser.ConfigParser()
configParser.read(configFile)

INDEXTYPE = configParser.get('global', 'index_type')
configParserLogger.info('index type: ' + INDEXTYPE)
MMAP = configParser.getint('global', 'mmap')
configParserLogger.info('mmap: ' + str(MMAP))

class IndexHandlerFactory():

    @staticmethod
    def Get():
        global INDEXTYPE
        if INDEXTYPE == 'UncompressIndex':
            return UncompressIndexHandler()
        else:
            raise Exception('unknown index type')

class IndexWriterFactory():

    @staticmethod
    def Get():
        global INDEXTYPE
        if INDEXTYPE == 'UncompressIndex':
            return UncompressIndexWriter()
        else:
            raise Exception('unknown index type')

class IndexReaderFactory():

    @staticmethod
    def Get():
        global INDEXTYPE, MMAP
        isMMap = False if MMAP == 0 else True
        if INDEXTYPE == 'UncompressIndex':
            return UncompressIndexReader(isMMap)
        else:
            raise Exception('unknown index type')

class IndexMergerFactory():

    @staticmethod
    def Get():
        global INDEXTYPE
        if INDEXTYPE == 'UncompressIndex':
            return UncompressIndexMerger()
        else:
            raise Exception('unknown index type')
