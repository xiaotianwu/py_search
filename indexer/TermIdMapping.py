import cPickle as pickle

class TermIdMappingHandler:
    @staticmethod
    def build_termid_mapping(termListFileName, mappingFileName):
        mapping = {}
        with open(termListFileName, 'r') as termListFile:
            termList = termListFile.readlines()
            termId = 0
            for term in termList:
                term = term.replace('\r','').replace('\n','')
                mapping[term] = termId
                termId += 1
            mappingToStore = pickle.dumps(mapping, True)
        with open(mappingFileName, 'wb') as mappingFile:
            mappingFile.write(mappingToStore)

    @staticmethod
    def read_termid_mapping(mappingFileName):
        mappingFile = open(mappingFileName, 'rb')
        mapping = pickle.loads(mappingFile.read())
        mappingFile.close()
        return mapping
