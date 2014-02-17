import sys
sys.path.append('../common')

from HtmlParser import TermExtractor

class SimpleIndexBuilder:
    def read(self, htmlFile):
        html = open(htmlFile, 'r').read()
        termExtractor = TermExtractor()
        termExtractor.set_stopwords('StopWordsList.txt')
        termExtractor.debug = True
        termExtractor.feed(html.read())
        html.close()
