#!/usr/bin/python

from HtmlParser import ExtendedHTMLParser

parser = ExtendedHTMLParser();
parser.feed(open('Sample.qq.html','r').read())

print parser.fanoutLink
