#!/usr/bin/python

from HtmlParser import ExtendedHTMLParser

parser = ExtendedHTMLParser();
parser.feed(open('Sample.yahoo.html','r').read())

print '----------------Split---------------------'
print 'link list =', parser.link
print 'term list =', parser.term
