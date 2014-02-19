import cPickle as pickle

class IntermediateGenerator:
    @staticmethod
    def build_page_docid_mapping(self, directory, mappingFileName, debug = False):
        files = DirHandler.get_all_files(directory, '*.page', False)
        mapping = {}
        docid = 0
        for f in files:
            mapping[docid] = f
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
    def read_page_docid_mapping(self, mappingFileName):
        mappingFile = open(mappingFileName, 'rb')
        mapping = pickle.loads(mappingFile.read())
        mappingFile.close()
        return mapping
