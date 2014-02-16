#!/usr/bin/python

from CrawlerImpl import UrlCrawler

crawler = UrlCrawler(debug = True)
crawler.init('http://www.yahoo.com')
crawler.run()

print crawler.urlPages
