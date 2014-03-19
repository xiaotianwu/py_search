#!/usr/bin/python

import os
import ConfigParser

from common.Logger import Logger
from common.simple_index.SimpleIndex import *

configParserLogger = Logger.Get('IndexConfig')

configFile = os.environ['PY_SEARCH_ROOT'] + '/config/IndexServe.conf'
configParserLogger.info('read config file: ' + configFile)
configParser = ConfigParser.ConfigParser()
configParser.read(configFile)

INDEXTYPE = configParser.get('global', 'index_type')
configParserLogger.info('index type: ' + INDEXTYPE)
MMAP = configParser.getint('global', 'mmap')
configParserLogger.info('mmap: ' + str(MMAP))
INDEXFOLDER = configParser.get('global', 'index_folder')
configParserLogger.info('index folder: ' + INDEXFOLDER)
INDEXMAPPING = configParser.get('index_file', 'mapping')
configParserLogger.info('mapping string: ' + INDEXMAPPING)

class IndexHandlerFactory():
    @staticmethod
    def Get():
        global INDEXTYPE
        if INDEXTYPE == 'SimpleIndex':
            return SimpleIndexHandler()
        else:
            raise Exception('unknown index type')

class IndexWriterFactory():
    @staticmethod
    def Get():
        global INDEXTYPE
        if INDEXTYPE == 'SimpleIndex':
            return SimpleIndexWriter()
        else:
            raise Exception('unknown index type')

class IndexReaderFactory():
    @staticmethod
    def Get():
        global INDEXTYPE, MMAP
        isMMap = False if MMAP == 0 else True
        if INDEXTYPE == 'SimpleIndex':
            return SimpleIndexReader(isMMap)
        else:
            raise Exception('unknown index type')

class IndexMergerFactory():
    @staticmethod
    def Get():
        global INDEXTYPE
        if INDEXTYPE == 'SimpleIndex':
            return SimpleIndexMerger()
        else:
            raise Exception('unknown index type')
