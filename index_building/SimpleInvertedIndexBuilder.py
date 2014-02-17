
sys.path.append('../common')

from HtmlParser import TermExtractor
from InvertedIndexBuilder import InvertedIndexBuilder

class SimpleInvertedIndexBuilder(InvertedIndexBuilder):
    def __init__(self):
        InvertedIndexBuilder.__init__(self)

    def build_from_html(self, htmlFile):
        html = open(htmlFile, 'r').read()
        termExtractor = TermExtractor()
        html.close()
