#!/usr/bin/python

import re
import os
from CrawlerImpl import UrlCrawlingThread
from CrawlerImpl import urlChunk
from CrawlerImpl import pageChunkPath
from CrawlerImpl import UrlCrawler

UrlCrawler.global_init(downloadPath = pageChunkPath)

if not os.path.exists(pageChunkPath):
    print pageChunkPath, 'not exists, create it'
    os.mkdir(pageChunkPath)

urlRegex = [re.compile('.*\.yahoo\.com/.*')]
threads = [UrlCrawlingThread(debug = True) for i in range(0, 5)]
for t in threads:
    t.init('http://www.yahoo.com', pagesLimit = 1000, crawlInterval = 1, timeout = 5, urlFilterRegexCollection = urlRegex)
    t.start()

for t in threads:
    t.join()

print 'urlChunkSize:', len(urlChunk)
print urlChunk
