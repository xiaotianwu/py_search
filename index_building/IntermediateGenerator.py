import cPickle as pickle
import sys
import os.path
sys.path.append('../common')

from Common import DirHandler
from Common import UrlFileNameConverter

class IntermediateGenerator:
    @staticmethod
    def build_page_docid_mapping(directory, mappingFileName, debug = False):
        files = DirHandler.get_all_files(directory, '*', False)
        mapping = {}
        docid = 0
        for fileName in files:
            baseName = os.path.basename(fileName)
            pageAddress = UrlFileNameConverter.filename_to_url(baseName)
            mapping[docid] = pageAddress
            docid += 1
        mappingToStore = pickle.dumps(mapping, True)       
        mappingFile = open(mappingFileName, 'wb')
        mappingFile.write(mappingToStore)
        mappingFile.close()
        if debug == True:
            debugFile = open(mappingFileName + '.debug', 'w')
            for (k, v) in mapping:
                debugFile.write(k + '\t' + v + '\n')
            debugFile.close()

    @staticmethod
    def read_page_docid_mapping(mappingFileName):
        mappingFile = open(mappingFileName, 'rb')
        mapping = pickle.loads(mappingFile.read())
        mappingFile.close()
        return mapping
