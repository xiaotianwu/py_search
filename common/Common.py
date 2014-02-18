import glob
import os

class UrlFileNameConverter:
    @staticmethod
    def url_to_filename(url):
        return url.replace('/', '^')

    @staticmethod
    def filename_to_url(fileName):
        # deal with the case of fileName is in absolute path
        fileName = fileName.split('/')[-1]
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
          
