import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from HTMLParser import HTMLParser
from Logger import Logger

class WordBreaker:
    def __init__(self):
        pass

    def Split(self, sentence):
        pass

# a simple wordbreaker based on space splitting, will be moved to common folder later
class SimpleWordBreaker(WordBreaker):
    def __init__(self):
        pass

    def Split(self, sentence):
        return sentence.split(' ')

class TermExtractor(HTMLParser):
    __tagClassification = 'UNKNOWN'
    __textTagRegex = re.compile('(p)|(h[1-6])|(em)|(a)|(base)')
    __regularWordRegex = re.compile('[a-zA-Z]+')

    def __init__(self):
        HTMLParser.__init__(self)
        self._wordBreaker = SimpleWordBreaker()
        self._logger = Logger.Get('HtmlParser')
        self.term = set()
        self.stopwords = set()

    def close(self):
        try:
            HTMLParser.close(self)
        except Exception as exception:
            print exception
        finally:
            self.term.clear()

    def SetStopwords(self, stopwordsFileName):
        languageSectionRegex = re.compile('\[[a-z][a-z]\-[a-z][a-z]\]')
        with open(stopwordsFileName, 'r') as stopwordsFile:
            for line in stopwordsFile.readlines():
                if (len(line) == 0 or line[0] == '#' or
                       languageSectionRegex.match(line)):
                    continue
                self.stopwords.add(
                    line.replace('\r', '').replace('\n', '').lower())

    def FilterWord(self, word):
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
                self._logger.debug("Tag = " + tag)
                self._logger.debug("Attrs = " + tag)
            else:
                self.__tagClassification = 'UNKNOWN'
        except Exception as exception:
            print(exception)

    def handle_data(self, data):
        try:
            self._logger.debug("Data = " + data)
            if self.__tagClassification in ('LINK', 'TEXT'):
                words = self._wordBreaker.Split(data);
                for word in words:
                    word = self.FilterWord(word)
                    if word != None:
                        self.term.add(word)
        except Exception as exception:
            print(exception)

class LinkExtractor(HTMLParser):
    __tagClassification = 'UNKNOWN'
    __linkTagRegex = re.compile('(a)|(base)')

    def __init__(self):
        HTMLParser.__init__(self)
        self.link = set()
        self._logger = Logger.Get('HtmlParser')

    def handle_starttag(self, tag, attrs):
        if self.__linkTagRegex.match(tag):
            if len(attrs) == 0:
                self.__tagClassification = 'UNKNOWN'
            else:
                for (name, value) in attrs:
                    if name == 'href':
                        self.link.add(value)
                self.__tagClassification = 'LINK'
                self._logger.debug("Tag = " + tag)
                self._logger.debug("Attrs = " + tag)
        else:
            self.__tagClassification = 'UNKNOWN'

    def close(self):
        try:
            HTMLParser.close(self)
        except Exception as exception:
            print exception
        finally:
            self.link.clear()
