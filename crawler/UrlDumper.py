# leveldb storage is recommended
USE_LEVELDB = False

import threading

try:
    import leveldb
    print('use leveldb storage')
    USE_LEVELDB = True
except ImportError as error:
    print(str(error) + 'use plain storage')
    from common.Common import UrlFileNameConverter as Converter

class UrlDumper:
    '''singleton dumper'''
    __db = None
    __path = None
    __dbLock = threading.RLock()
    __initialized = False

    @staticmethod
    def Init(chunkPath, leveldbFolder):
        global USE_LEVELDB
        UrlDumper.__dbLock.acquire()
        if UrlDumper.__initialized == True:
            UrlDumper.__dbLock.release()
            return
        UrlDumper.__path = chunkPath
        if USE_LEVELDB == True and UrlDumper.__db == None:
            dbFolder = UrlDumper.__path + '/' + leveldbFolder
            print('create db foler:' + dbFolder)
            UrlDumper.__db = leveldb.LevelDB(dbFolder)
        UrlDumper.__initialized = True
        UrlDumper.__dbLock.release()

    @staticmethod
    def Write(url, page):
        if UrlDumper.__initialized == False:
            raise Exception('call init before writing')
        global USE_LEVELDB
        # leveldb is not thread safe
        if USE_LEVELDB == True:
            UrlDumper.__dbLock.acquire()
            UrlDumper.__db.Put(url, page)
            UrlDumper.__dbLock.release()
        else:
            fileName = Converter.UrlToFileName(url)
            try:
                absolutePath = UrlDumper.__path + '/' + fileName
                print 'write to file', absolutePath
                with open(absolutePath, 'w') as pageFile:
                    pageFile.write(page)
            except IOError as error:
                print(error)

    @staticmethod
    def Read(url):
        if UrlDumper.__initialized == False:
            raise Exception('call init before writing')
        global USE_LEVELDB
        if USE_LEVELDB == True:
            UrlDumper.__dbLock.acquire()
            page = UrlDumper.__db.Get(url)
            UrlDumper.__dbLock.release()
            return page
        else:
            fileName = Converter.UrlToFileName(url)
            try:
                absolutePath = UrlDumper.__path + '/' + fileName
                print 'read from file', absolutePath
                with open(absolutePath, 'r') as pageFile:
                    return pageFile.read()
            except IOError as error:
                print(error)
                return None
