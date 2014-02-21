import copy
import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

import cPickle as pickle
from HtmlParser import TermExtractor
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader
from SimpleIndex import SimpleIndexWriter
from Common import UrlFileNameConverter
from Common import DirHandler
from IntermediateGenerator import IntermediateGenerator

class SimpleIndexBuilder:
    def __init__(self, debug = False):
        self.__termExtractor = TermExtractor()
        self.__termExtractor.debug = debug
        self.__debug = debug
        self.__index = {}

    def init(self, mappingFile, stopwordsFile):
        self.__termExtractor.set_stopwords(stopwordsFile)
        self.__docid_page_mapping = IntermediateGenerator.read_page_docid_mapping(mappingFile)
        print self.__docid_page_mapping

    def build_index(self, inputDir, outputName):
        self._parse_page_in_dir(inputDir)
        self._build_inverted_index(outputName)

    def _parse_page(self, pageFile):
        if self.__debug == True:
            print 'current parsing:', pageFile
        page = open(pageFile, 'r')
        try:
            self.__termExtractor.feed(page.read())
            print 'term extracted =', self.__termExtractor.term
            pageAddress = UrlFileNameConverter.filename_to_url(pageFile)
            docid = self.__docid_page_mapping[pageAddress]
            if docid in self.__index:
                print 'pageAddress =', pageAddress, 'docid =', docid, 'has been parsed, skip it'
            else:
                self.__index[docid] = copy.deepcopy(self.__termExtractor.term)
        except Exception, exception:
            print exception
        finally:
            self.__termExtractor.term.clear()
            self.__termExtractor.close()
            page.close()
        
    def _parse_page_in_dir(self, directory):
        files = DirHandler.get_all_files(directory)
        for f in files:
            self._parse_page(f)

    def _build_inverted_index(self, indexFileName):
        invertedIndex = SimpleIndex()
        for (docid, terms) in self.__index.items():
            print 'docid =', docid, 'terms =', terms
            for t in terms:
                invertedIndex.add_term_docid(t, docid)
        writer = SimpleIndexWriter()
        writer.write(invertedIndex, indexFileName)
