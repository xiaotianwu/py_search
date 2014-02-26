import cPickle as pickle
import sys
import os.path
sys.path.append('../common')

from Common import DirHandler
from Common import UrlFileNameConverter

class DocIdMappingGen:
    @staticmethod
    def build_page_docid_mapping(directory, mappingFileName):
        files = DirHandler.get_all_files(directory, '*', False)
        mapping = {}
        docid = 0
        for fileName in files:
            baseName = os.path.basename(fileName)
            pageAddress = UrlFileNameConverter.filename_to_url(baseName)
            mapping[pageAddress] = docid
            docid += 1
        mappingToStore = pickle.dumps(mapping, True)       
        with open(mappingFileName, 'wb') as mappingFile:
            mappingFile.write(mappingToStore)

    @staticmethod
    def read_page_docid_mapping(mappingFileName):
        mappingFile = open(mappingFileName, 'rb')
        mapping = pickle.loads(mappingFile.read())
        mappingFile.close()
        return mapping
