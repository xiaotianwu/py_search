#!/usr/bin/python

import os
from CrawlerImpl import UrlCrawler
from CrawlerImpl import UrlCrawlingThread
from CrawlerImpl import urlChunk
from CrawlerImpl import pageChunkPath

if not os.path.exists(pageChunkPath):
    print pageChunkPath, 'not exists, create it'
    os.mkdir(pageChunkPath)

crawler = UrlCrawler(proxies = {}, debug = False)
crawler.init('http://www.yahoo.com', 10, 0.01, 5)
crawler.run()

print crawler.urlPages
print '-------------------------------------------'
urlChunk.clear()

threads = [UrlCrawlingThread(debugOpen = False) for i in range(0, 5)]
for t in threads:
    t.init('http://www.yahoo.com')
    t.start()

for t in threads:
    t.join()

print 'urlChunkSize:', len(urlChunk)
print urlChunk
