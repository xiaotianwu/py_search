#!/usr/bin/python

from HtmlParser import LinkExtractor
from HtmlParser import TermExtractor

if __name__ == '__main__':
    parser = LinkExtractor();
    parser.feed(open('Sample.yahoo.html','r').read())
    
    print 'link list =', parser.link
    print '----------------Split---------------------'
    
    parser = TermExtractor()
    parser.set_stopwords('StopWordsList.txt')
    print 'stop words = ', parser.stopwords
    
    parser.debug = True
    fileName = 'Sample.yahoo.html'
    parser.feed(open(fileName, 'r').read())
    print 'term list =', parser.term
