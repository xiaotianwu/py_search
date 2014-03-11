#!/usr/bin/python

import logging

from HtmlParser import LinkExtractor
from HtmlParser import TermExtractor

if __name__ == '__main__':
    parser = LinkExtractor();
    parser.feed(open('../test_data/Sample.yahoo.html','r').read())
    print('link list =', parser.link)
    print('----------------Split---------------------')
    parser.close()

    parser = TermExtractor()
    parser.SetStopwords('../config/StopWordsList.txt')
    print('stop words = ', parser.stopwords)
    fileName = '../test_data/Sample.yahoo.html'
    parser.feed(open(fileName, 'r').read())
    print('term list =', parser.term)
    parser.close()
