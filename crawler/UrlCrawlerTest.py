#!/usr/bin/python

import os
import re
import shutil

from UrlCrawler import UrlCrawler

if __name__ == '__main__':
    urlRegex1 = re.compile('http://oj.leetcode.com/discuss.*')
    urlRegex2 = re.compile('http://oj.leetcode.com/question.*')
    urlRegex = [urlRegex1, urlRegex2]
    crawler = UrlCrawler()
    crawler.Init(0, 0, 0, urlRegex)
    assert crawler._FilterUrl('http://oj.leetcode.com/discuss/1') == True
    assert crawler._FilterUrl('http://oj.leetcode.com/question/1') == True
    assert crawler._FilterUrl('http://www.google.com') == False
    
    path = './test/'
    seedUrl = 'http://www.yahoo.com'
    UrlCrawler.GlobalInit(seedUrl, path)

    crawler = UrlCrawler()
    crawler.Init(pagesLimit = 10, crawlInterval = 0.5, timeout = 5,
                 urlFilterRegexCollection = None)
    crawler.Run()
    print crawler.GetUrlChunk()    

    UrlCrawler.GlobalExit()
    shutil.rmtree(path)
