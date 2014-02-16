#!/usr/bin/python

p = ExtendedHTMLParser()
p.set_stopwords('StopWordsList.txt')
crawler = UrlCrawler("http://www.yahoo.com", p, crawlLimit = 1000)
crawler.run()

