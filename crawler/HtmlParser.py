import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from HTMLParser import HTMLParser

# Import stop words
#class Preprocessor:
#    def __init__(self):
#        pass

# a simple wordbreaker based on space splitting, will be moved to common folder later
class WordBreaker:
    def __init__(self):
        pass

    def split(self, sentence):
        return [word.strip() for word in sentence.split(' ') if word.strip() != '']

class ExtendedHTMLParser(HTMLParser):
    debugOutput = False
    link = []
    term = []
    tagClassification = 'UNKNOWN'
    linkTagRegex = re.compile('(a)|(base)')
    textTagRegex = re.compile('(p)|(h[1-6])|(em)')
    wordBreaker = WordBreaker()

    def set_debug(self, debug):
        self.debugOutput = debug
        
    def handle_starttag(self, tag, attrs):
        if self.linkTagRegex.match(tag):
            if len(attrs) == 0:
                self.tagClassification = 'UNKNOWN'
            else:
                for (name, value) in attrs:
                    if name == 'href':
                        self.link.append(value)
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
            

    def handle_data(self, data):
        if self.debugOutput == True:
            print "Data =", data
        if self.tagClassification in ('LINK', 'TEXT'):
            words = self.wordBreaker.split(data);
            self.term += words
