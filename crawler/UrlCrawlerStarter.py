#!/usr/bin/python

import re
import os

from UrlCrawler import UrlCrawlingThread
from UrlCrawler import UrlCrawler

if __name__ == '__main__':
    url = 'http://www.yahoo.com'
    path = '../page_chunk'
    UrlCrawler.GlobalInit(seedUrl = url,
                          downloadPath = path)
    
    if not os.path.exists(path):
        print path, 'not exists, create it'
        os.mkdir(path)
    
    urlRegex = [re.compile('.*\.yahoo\.com/.*')]
    threads = [UrlCrawlingThread() for i in range(0, 5)]
    for th in threads:
        th.Init(pagesLimit = 1000,
                crawlInterval = 5,
                timeout = 5,
                urlFilterRegexCollection = urlRegex)
        th.start()
    
    for th in threads:
        th.join()
    
    print 'urlChunkSize:', len(UrlCrawler.GetUrlChunk())
