import glob
import os
import os.path
import random
import thread
from multiprocessing.pool import ThreadPool

THREAD_POOL_SIZE = 4

class Locking():
    '''local locking'''
    def __init__(self, locker):
        self._locker = locker

    def __enter__(self):
        self._locker.acquire()

    def __exit__(self, e_t, e_v, e_b):
        self._locker.release()

def InitThreadPool():
    Async.pool = ThreadPool(processes = THREAD_POOL_SIZE)

def UninitThreadPool():
    Async.pool.close()

def Async(decoratedFunc):
    '''decorator of using thread pool'''
    def AsyncCall(*args, **opts):
        Async.pool.apply_async(decoratedFunc, args, opts)
    return AsyncCall

def AsyncThread(decoratedFunc):
    '''using an anonymous thread which is not in the thead pool'''
    def async_call(*args, **opts):
        thread.start_new_thread(decoratedFunc, args, opts)
    return async_call

def CallBack(decoratedFunc):
    '''it's just a qualifier'''
    return decoratedFunc

def LeftPadding(string, length, paddingChar = ' '):
    '''if string is abc, length is 5
       paddingChar is *, output is **abc'''
    if len(string) >= length:
        return string
    else:
        return paddingChar * (length - len(string)) + string

def RightPadding(string, length, paddingChar = ' '):
    '''if string is abc, length is 5
       paddingChar is *, output is abc**'''
    if len(string) >= length:
        return string
    else:
        return string + paddingChar * (length - len(string))

class UrlFileNameConverter:
    @staticmethod
    def UrlToFileName(url):
        '''convert http://www to http:^^www'''
        return url.replace('/', '^')

    @staticmethod
    def FileNameToUrl(fileName):
        '''convert http:^^www to http://www'''
        fileName = os.path.basename(fileName)
        return fileName.replace('^', '/')

class DirHandler:
    @staticmethod
    def GetAllFiles(directory, suffix = '*', recursive = False):
        '''get all files under specified folder'''
        path = directory + '/' + suffix
        entries = glob.glob(path)
        files = []
        dirs = []
        for entry in entries:
            if os.path.isfile(entry):
                files.append(entry)
            elif os.path.isdir(entry):
                dirs.append(entry)
            elif os.path.islink(entry):
                pass
        if recursive == True:
            for dirEntry in dirs:
                files += DirHandler.GetAllFiles(dirEntry, suffix, True)
        return files

def GenRandomIndex():
    i = 0
    s = set()
    randomIndexLen = 1000
    while i < randomIndexLen:
        item = random.randint(0, 10000)
        if item in s:
            continue
        else:
            s.add(item)
            i += 1
    return s

