#!/usr/bin/python

from HtmlParser import LinkExtractor
from HtmlParser import TermExtractor

#parser = LinkExtractor();
#parser.feed(open('Sample.yahoo.html','r').read())
#
#print 'link list =', parser.link
#print '----------------Split---------------------'
#
parser = TermExtractor()
parser.set_stopwords('StopWordsList.txt')
print 'stop words = ', parser.stopwords

parser.debug = True
fileName = '../page_chunk/https:^^search.yahoo.com^search?ei=UTF-8&fr=fp-tts-901&woeid=23424856&p=Vicenza,%20Veneto,%20Italy'
#fileName = 'Sample.yahoo.html'
parser.feed(open(fileName, 'r').read())
print 'term list =', parser.term
