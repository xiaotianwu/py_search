import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from HTMLParser import HTMLParser

class WordBreaker:
    def __init__(self):
        pass

    def split(self, sentence):
        pass

# a simple wordbreaker based on space splitting, will be moved to common folder later
class SimpleWordBreaker(WordBreaker):
    def __init__(self):
        pass

    def split(self, sentence):
        return sentence.split(' ')

class TermExtractor(HTMLParser):
    __tagClassification = 'UNKNOWN'
    __textTagRegex = re.compile('(p)|(h[1-6])|(em)|(a)|(base)')
    __regularWordRegex = re.compile('[a-zA-Z]+')

    _wordBreaker = SimpleWordBreaker()

    debug = False
    term = set()
    stopwords = set()
    
    def set_stopwords(self, stopwordsFile):
        languageSectionRegex = re.compile('\[[a-z][a-z]\-[a-z][a-z]\]')
        for line in open(stopwordsFile, 'r').readlines():
            if (len(line) == 0 or line[0] == '#' or
                   languageSectionRegex.match(line)):
                continue
            self.stopwords.add(line.replace('\r', '').replace('\n', '').lower())

    def filter_word(self, word):
        word = word.strip().lower()
        if len(word) == 0 or word in self.stopwords:
            return None
        elif not self.__regularWordRegex.match(word):
            return None
        else:
            return word

    def handle_starttag(self, tag, attrs):
        try:
            if self.__textTagRegex.match(tag):
                self.__tagClassification = 'TEXT'
                if self.debug == True:
                    print "Tag =", tag
                    print "Attrs =", attrs
            else:
                self.__tagClassification = 'UNKNOWN'
        except Exception, exception:
            print exception

    def handle_data(self, data):
        try:
            if self.debug == True:
                print "Data =", data
            if self.__tagClassification in ('LINK', 'TEXT'):
                words = self._wordBreaker.split(data);
                for word in words:
                    word = self.filter_word(word)
                    if word != None:
                        self.term.add(word)
        except Exception, exception:
            print exception

class LinkExtractor(HTMLParser):
    __tagClassification = 'UNKNOWN'
    __linkTagRegex = re.compile('(a)|(base)')

    debug = False
    link = set()

    def handle_starttag(self, tag, attrs):
        if self.__linkTagRegex.match(tag):
            if len(attrs) == 0:
                self.__tagClassification = 'UNKNOWN'
            else:
                for (name, value) in attrs:
                    if name == 'href':
                        self.link.add(value)
                self.__tagClassification = 'LINK'
                if self.debug == True:
                    print "Tag =", tag
                    print "Attrs =", attrs
        else:
            self.__tagClassification = 'UNKNOWN'
