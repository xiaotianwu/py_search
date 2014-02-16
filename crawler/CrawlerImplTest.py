#!/usr/bin/python

import os
import re
import shutil

from CrawlerImpl import UrlCrawler

path = './test/'
UrlCrawler.global_init(downloadPath = path)

urlRegex1 = re.compile('^http://oj.leetcode.com/discuss.*')
urlRegex2 = re.compile('^http://oj.leetcode.com/question.*')
urlRegex = [urlRegex1, urlRegex2]
crawler = UrlCrawler()
crawler.init('.', 0, 0, 0, urlRegex)
assert crawler._filter_url('http://oj.leetcode.com/discuss/1') == True
assert crawler._filter_url('http://oj.leetcode.com/question/1') == True
assert crawler._filter_url('http://www.google.com') == False

print '-------------------------'
crawler = UrlCrawler(debug = True)
crawler.init('http://oj.leetcode.com/discuss/questions', pagesLimit = 10,
             crawlInterval = 0.5, timeout = 5,
             urlFilterRegexCollection = urlRegex)
crawler.run()

print crawler._urlPages
shutil.rmtree(path)
