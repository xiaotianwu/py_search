#!/usr/bin/python

import os
import re
from CrawlerImpl import UrlCrawler
from CrawlerImpl import UrlCrawlingThread
from CrawlerImpl import urlChunk
from CrawlerImpl import pageChunkPath

urlRegex1 = re.compile('^http://oj.leetcode.com/discuss.*')
urlRegex2 = re.compile('^http://oj.leetcode.com/question.*')
urlRegex = [urlRegex1, urlRegex2]
crawler =UrlCrawler()
crawler.init(urlFilterRegexCollection = urlRegex)
assert crawler.filter_url('http://oj.leetcode.com/discuss/1') == True
assert crawler.filter_url('http://oj.leetcode.com/question/1') == True
assert crawler.filter_url('http://www.google.com') == False

if not os.path.exists(pageChunkPath):
    print pageChunkPath, 'not exists, create it'
    os.mkdir(pageChunkPath)

crawler = UrlCrawler(proxies = {}, debug = True)
crawler.init('http://oj.leetcode.com/discuss/questions', 10, 2, 5)
crawler.run()

print crawler.urlPages
print '-------------------------------------------'
urlChunk.clear()

threads = [UrlCrawlingThread(debugOpen = True) for i in range(0, 5)]
for t in threads:
    t.init('http://www.yahoo.com')
    t.start()

for t in threads:
    t.join()

print 'urlChunkSize:', len(urlChunk)
print urlChunk
