try:
    import leveldb
    USE_LEVELDB = True
except ImportError as error:
    print(str(error) + 'use plain storage')
    from common.Common import UrlFileNameConverter as Converter
    USE_LEVELDB = False

class UrlDumper:
    '''singleton dumper'''
    __db = None
    __path = None

    def __init__(self, chunkPath):
        global USE_LEVELDB
        if USE_LEVELDB == True and UrlDumper.__db == None:
            UrlDumper.__path = chunkPath
            dbFile = UrlDumper.__path + 'urlPages'
            print(dbFile)
            UrlDumper.__db = leveldb.LevelDB(dbFile)

    def Write(self, url, content):
        global USE_LEVELDB
        if USE_LEVELDB == True:
            UrlDumper.__db.Put(url, content)
        else:
            fileName = Converter.UrlToFileName(url)
            try:
                with open(UrlDumper.__path + fileName, 'w') as pageFile:
                    pageFile.write(page)
            except IOError as error:
                print(error)

    def Read(self, url):
        global USE_LEVELDB
        if USE_LEVELDB == True:
            UrlDumper.__db.Get(url)
        else:
            fileName = Converter.UrlToFileName(url)
            try:
                with open(UrlDumper.__path + fileName, 'r') as pageFile:
                     return pageFile.read()
            except IOError as error:
                print(error)
                return None
