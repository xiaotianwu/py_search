#!/usr/bin/python

import os
import re
from CrawlerImpl import UrlCrawler

urlRegex1 = re.compile('^http://oj.leetcode.com/discuss.*')
urlRegex2 = re.compile('^http://oj.leetcode.com/question.*')
urlRegex = [urlRegex1, urlRegex2]
crawler =UrlCrawler()
crawler.init('.', 0, 0, 0, urlRegex)
assert crawler.filter_url('http://oj.leetcode.com/discuss/1') == True
assert crawler.filter_url('http://oj.leetcode.com/question/1') == True
assert crawler.filter_url('http://www.google.com') == False

crawler = UrlCrawler(debug = True)
crawler.init('http://oj.leetcode.com/discuss/questions', pagesLimit = 10, crawlInterval = 0.5, timeout = 3, urlFilterRegexCollection = urlRegex)
crawler.run()

print crawler.urlPages
