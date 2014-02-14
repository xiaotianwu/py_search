import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from HTMLParser import HTMLParser

# a simple wordbreaker based on space splitting, will be moved to common folder later
class SimpleWordBreaker:
    def __init__(self):
        pass

    def split(self, sentence):
        return sentence.split(' ')

class ExtendedHTMLParser(HTMLParser):
    debugOutput = False
    link = set()
    term = set()
    stopwords = set()
    tagClassification = 'UNKNOWN'
    linkTagRegex = re.compile('(a)|(base)')
    textTagRegex = re.compile('(p)|(h[1-6])|(em)')
    regularWordRegex = re.compile('[a-zA-Z]+')
    wordBreaker = SimpleWordBreaker()

    def set_stopwords(self, stopwordsFile):
        languageSectionRegex = re.compile('\[[a-z][a-z]\-[a-z][a-z]\]')
        for line in open(stopwordsFile, 'r').readlines():
            if len(line) == 0 or line[0] == '#' or languageSectionRegex.match(line):
                pass
            self.stopwords.add(line.replace('\r', '').replace('\n', '').lower())

    def set_wordbreaker(self, wb):
        self.wordBreaker = wb

    def set_debug(self, debug):
        self.debugOutput = debug
        
    def handle_starttag(self, tag, attrs):
        if self.linkTagRegex.match(tag):
            if len(attrs) == 0:
                self.tagClassification = 'UNKNOWN'
            else:
                for (name, value) in attrs:
                    if name == 'href':
                        self.link.add(value)
                self.tagClassification = 'LINK'
                if self.debugOutput == True:
                    print "Tag =", tag
                    print "Attrs =", attrs
        elif self.textTagRegex.match(tag):
            self.tagClassification = 'TEXT'
            if self.debugOutput == True:
                print "Tag =", tag
                print "Attrs =", attrs
        else:
            self.tagClassification = 'UNKNOWN'

    def filter_word(self, word):
        word = word.strip().lower()
        if len(word) == 0 or word in self.stopwords:
            return ''
        elif not self.regularWordRegex.match(word):
            return ''
        else:
            return word

    def handle_data(self, data):
        if self.debugOutput == True:
            print "Data =", data
        if self.tagClassification in ('LINK', 'TEXT'):
            words = self.wordBreaker.split(data);
            for word in words:
                word = self.filter_word(word)
                if word != '':
                    self.term.add(word)
