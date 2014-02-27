#!/usr/bin/python

import os
import re
import shutil
import sys
sys.path.append('../common')

from CrawlerImpl import UrlCrawler
from HtmlParser import LinkExtractor

if __name__ == '__main__':
    path = './test/'
    seedUrl = 'http://oj.leetcode.com/discuss/questions'
    UrlCrawler.global_init(seedUrl, path)
    
    urlRegex1 = re.compile('^http://oj.leetcode.com/discuss.*')
    urlRegex2 = re.compile('^http://oj.leetcode.com/question.*')
    urlRegex = [urlRegex1, urlRegex2]
    crawler = UrlCrawler()
    crawler.init(0, 0, 0, urlRegex, None)
    assert crawler._filter_url('http://oj.leetcode.com/discuss/1') == True
    assert crawler._filter_url('http://oj.leetcode.com/question/1') == True
    assert crawler._filter_url('http://www.google.com') == False
    
    print '-------------------------'
    crawler = UrlCrawler(debug = True)
    crawler.init(pagesLimit = 10,
                 crawlInterval = 0.5, timeout = 5,
                 urlFilterRegexCollection = urlRegex,
                 parser = LinkExtractor())
    crawler.run()
    
    print crawler._urlPages
    shutil.rmtree(path)
