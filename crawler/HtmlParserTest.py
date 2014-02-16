#!/usr/bin/python

from HtmlParser import LinkExtractor
from HtmlParser import TermExtractor

parser = LinkExtractor();
parser.feed(open('Sample.yahoo.html','r').read())

print 'link list =', parser.link
print '----------------Split---------------------'

parser = TermExtractor()
parser.set_stopwords('StopWordsList.txt')
parser.debug = True
parser.feed(open('Sample.yahoo.html','r').read())

print 'term list =', parser.term
print 'stop words = ', parser.stopwords
