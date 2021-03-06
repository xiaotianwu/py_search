# leveldb storage is recommended
USE_LEVELDB = False

import threading

from common.Common import Locking
from common.Logger import Logger

try:
    import leveldb
    USE_LEVELDB = True
except ImportError as error:
    print(str(error))
    from common.Common import UrlFileNameConverter as Converter

class UrlDumper:
    '''singleton dumper'''
    __db = None
    __path = None
    __dbLock = threading.RLock()
    __init = False
    __logger = Logger.Get('UrlDumper')

    @staticmethod
    def Init(chunkPath, leveldbFolder):
        global USE_LEVELDB
        with Locking(UrlDumper.__dbLock):
            if UrlDumper.__init == True:
                return
            UrlDumper.__path = chunkPath
            if USE_LEVELDB == True:
                dbFolder = UrlDumper.__path + '/' + leveldbFolder
                UrlDumper.__logger.info('use leveldb, create db folder:' +
                                        dbFolder)
                UrlDumper.__db = leveldb.LevelDB(dbFolder)
            else:
                UrlDumper.__logger.info('use plain storage file')
            UrlDumper.__init = True

    @staticmethod
    def Write(url, page):
        if UrlDumper.__init == False:
            raise Exception('call init before writing')
        global USE_LEVELDB
        # leveldb is not thread safe
        if USE_LEVELDB == True:
            UrlDumper.__logger.debug('write to leveldb, url: ' + url)
            with Locking(UrlDumper.__dbLock):
                UrlDumper.__db.Put(url, page)
        else:
            fileName = Converter.UrlToFileName(url)
            try:
                absolutePath = UrlDumper.__path + '/' + fileName
                UrlDumper.__logger.debug('write to file: ' + absolutePath)
                with open(absolutePath, 'w') as pageFile:
                    pageFile.write(page)
            except IOError as error:
                print(error)

    @staticmethod
    def Read(url):
        if UrlDumper.__init == False:
            raise Exception('call init before writing')
        global USE_LEVELDB
        if USE_LEVELDB == True:
            UrlDumper.__logger.debug('read from leveldb, url: ' + url)
            with Locking(UrlDumper.__dbLock):
                page = UrlDumper.__db.Get(url)
            return page
        else:
            fileName = Converter.UrlToFileName(url)
            try:
                absolutePath = UrlDumper.__path + '/' + fileName
                UrlDumper.__logger.debug('read from file: ' + absolutePath)
                with open(absolutePath, 'r') as pageFile:
                    return pageFile.read()
            except IOError as error:
                print(error)
                return None
