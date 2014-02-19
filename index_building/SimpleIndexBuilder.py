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
        self.__termExtractor.debug = True
        self.__debug = debug
        self.__index = {}

    def init(self, stopwordsFile = 'StopWordsList.txt', mappingFile)
        self.__termExtractor.set_stopwords(stopwordsFile)
        self.__docid_page_mapping = IntermediateGenerator.read_page_docid_mapping(mappingFile)
        
    def parse_page(self, pageFile):
        page = open(pageFile, 'r').read()
        try:
            self.__termExtractor.term.clear()
            self.__termExtractor.feed(page.read())
            pageAddress = UrlFileNameConverter.filename_to_url(pageFile)
            if pageAddress in self.__index:
                if self.__debug == True:
                    print pageAddress, 'has been parsed, skip it'
            else:
                docid = self.__docid_page_mapping[pageAddress]
                self.__index[docid] = self.__termExtractor.term
        except Exception, exception:
            print exception
        finally:
            page.close()

    def parse_page_in_dir(self, directory):
        files = DirHandler.get_all_files(directory, '', False)
        for f in files:
            self.parse_page(f)

    def build_inverted_index(self, indexFileName):
        invertedIndex = SimpleIndex()
        for (docid, terms) in self.__index:
            for t in terms:
                invertedIndex.add_term_docid(t, docid)
        writer = SimpleIndexWriter()
        writer.write(invertedIndex, indexFileName)
