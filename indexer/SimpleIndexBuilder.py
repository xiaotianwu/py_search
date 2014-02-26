import copy
import cPickle as pickle
import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from Common import DirHandler
from Common import UrlFileNameConverter
from Logger import Logger
from HtmlParser import TermExtractor
from DocIdMappingGen import DocIdMappingGen as MapGen
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader
from SimpleIndex import SimpleIndexWriter

class SimpleIndexBuilder:
    def __init__(self):
        self._logger = Logger.get('IndexBuilder')
        self._termExtractor = TermExtractor()
        self._index = {}

    def init(self, mappingFile, stopwordsFile):
        self._logger.info('StopWords File:' + stopwordsFile)
        self._termExtractor.set_stopwords(stopwordsFile)
        self._docid_page_mapping = MapGen.read_page_docid_mapping(mappingFile)
        print self._docid_page_mapping

    def build_index(self, inputDir, outputName):
        self._parse_page_in_dir(inputDir)
        self._build_inverted_index(outputName)

    def _parse_page(self, pageFile):
        self._logger.info('current parsing:' + pageFile)
        page = open(pageFile, 'r')
        try:
            self._termExtractor.feed(page.read())
            self._logger.debug('term extracted:' + str(self._termExtractor.term))
            print 
            pageAddress = UrlFileNameConverter.filename_to_url(pageFile)
            docid = self._docid_page_mapping[pageAddress]
            if docid in self._index:
                self._logger.warn('pageAddress:' + pageAddress +
                                  'docid:' + docid +
                                  'has been parsed, skip it' )
            else:
                self._index[docid] = copy.deepcopy(self._termExtractor.term)
        except Exception, exception:
            print exception
        finally:
            self._termExtractor.term.clear()
            self._termExtractor.close()
            page.close()
        
    def _parse_page_in_dir(self, directory):
        files = DirHandler.get_all_files(directory)
        for f in files:
            self._parse_page(f)

    def _build_inverted_index(self, indexFileName):
        invertedIndex = SimpleIndex()
        l1 = lambda x, y: x + y
        l2 = lambda x, y: [(subY, x) for subY in y]
        termDocPair = reduce(l1, [l2(key, self._index[key])
                                  for key in self._index.keys()])
        #print termDocPair
        del self._index
        for (term, docid) in termDocPair:
            invertedIndex.add_term_docid(term, docid)
        del termDocPair
        writer = SimpleIndexWriter()
        writer.write(invertedIndex, indexFileName)
