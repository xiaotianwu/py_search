import sys
sys.path.append('../common')
sys.path.append('../common/SimpleIndex')

from HtmlParser import TermExtractor
from SimpleIndex import SimpleIndex
from SimpleIndex import SimpleIndexReader
from SimpleIndex import SimpleIndexWriter
from Common import UrlFileNameConverter
from COmmon import DirHandler

class SimpleIndexBuilder:
    def __init__(self, debug = False):
        self.__termExtractor = TermExtractor()
        self.__termExtractor.debug = True
        self.__debug = debug
        self.__index = dict()
        self.__invertedIndex = SimpleIndex()

    def init(self, stopwordsFile = 'StopWordsList.txt')
        self.__termExtractor.set_stopwords(stopwordsFile)
        
    def parse_html(self, htmlFile):
        html = open(htmlFile, 'r').read()
        try:
            self.__termExtractor.term.clear()
            self.__termExtractor.feed(html.read())
            htmlAddress = UrlFileNameConverter.filename_to_url(htmlFile)
            if htmlAddress in self.__index:
                if self.__debug == True:
                    print htmlAddress, 'has been parsed, skip it'
            else:
                self.__index[htmlAddress] = self.__termExtractor.term
        except Exception, exception:
            print exception
        finally:
            html.close()

    def parse_html_dir(self, directory, recursive = False):
        files = DirHandler.get_all_files(directory, '*.html', recursive)
        for f in files:
            self.parse_html(f)

    def build_inverted_index(self):
        pass
