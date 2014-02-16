#!/usr/bin/python

from HtmlParser import ExtendedHTMLParser

parser = ExtendedHTMLParser();
parser.set_stopwords('StopWordsList.txt')
parser.feed(open('Sample.yahoo.html','r').read())

print '----------------Split---------------------'
print 'stop words = ', parser.stopwords
print 'link list =', parser.link
print 'term list =', parser.term

parser.debug = True
parser.feed(open('Sample.yahoo.html','r').read())
