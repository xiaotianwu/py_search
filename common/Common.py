import glob
import os
import os.path
import thread
from multiprocessing.pool import ThreadPool

THREAD_POOL_SIZE = 4

def InitThreadPool():
    async.pool = ThreadPool(processes = THREAD_POOL_SIZE)

def UninitThreadPool():
    async.pool.close()

def async(decoratedFunc):
    def async_call(*args, **opts):
        async.pool.apply_async(decoratedFunc, args, opts)
    return async_call

def async_thread(decoratedFunc):
    '''using an anonymous thread which is not in the thead pool'''
    def async_call(*args, **opts):
        thread.start_new_thread(decoratedFunc, args, opts)
    return async_call

def call_back(decoratedFunc):
    '''it's just a qualifier'''
    return decoratedFunc

class UrlFileNameConverter:
    @staticmethod
    def url_to_filename(url):
        return url.replace('/', '^')

    @staticmethod
    def filename_to_url(fileName):
        # deal with the case of fileName is in absolute path
        fileName = os.path.basename(fileName)
        return fileName.replace('^', '/')

class DirHandler:
    @staticmethod
    def get_all_files(directory, suffix = '*', recursive = False):
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
                files += DirHandler.get_all_files(dirEntry, suffix, True)
        return files
