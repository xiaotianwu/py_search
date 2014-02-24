#!/usr/bin/python

import re
import os

from CrawlerImpl import UrlCrawlingThread
from CrawlerImpl import urlChunk
from CrawlerImpl import pageChunkPath
from CrawlerImpl import UrlCrawler

if __name__ == '__main__':
    UrlCrawler.global_init(seedUrl = 'http://www.yahoo.com',
                           downloadPath = pageChunkPath)
    
    if not os.path.exists(pageChunkPath):
        print pageChunkPath, 'not exists, create it'
        os.mkdir(pageChunkPath)
    
    urlRegex = [re.compile('.*\.yahoo\.com/.*')]
    threads = [UrlCrawlingThread(debug = True) for i in range(0, 5)]
    i = 0
    for t in threads:
        t.init(crawlerId = i, pagesLimit = 1000,
               urlFilterRegexCollection = urlRegex)
        t.start()
        i += 1
    
    for t in threads:
        t.join()
    
    print 'urlChunkSize:', len(urlChunk)
    print urlChunk
