try:
    import leveldb
    USE_LEVELDB = True
except ImportError as error:
    print(str(error) + 'use plain storage')
    from common.Common import UrlFileNameConverter
    USE_LEVELDB = False

# global chunk path
pageChunkPath = '../page_chunk/'

class UrlDumper:
    __db = None

    def __init__(self, chunkPath = pageChunkPath):
        global USE_LEVELDB
        if USE_LEVELDB == True:
            dbFile = chunkPath + 'urlPages'
            print(dbFile)
            if UrlDumper.__db == None:
                UrlDumper.__db = leveldb.LevelDB(dbFile)
        else:
            pass

    def Write(self, url, content):
        if USE_LEVELDB == True:
            UrlDumper.__db.Put(url, content)
        else:
            pass
