import re
import Queue
import urllib
import threading
from threading import Thread

class UrlCrawler:
    seedUrl = ''
    crawlPagesLimit = 0
    proxies = {}
    urlPages = {}
    
    def __init__(self, seedUrl, crawlPagesLimit = 10, proxies = {}):
        self.seedUrl = seedUrl
        self.crawlPagesLimit = crawlPagesLimit
        self.proxies = proxies

    def GetFanoutLink(self, page_text):
        parser = ExtendedHTMLParser()
        try:
            parser.feed(page_text)
        except Exception, exception:
            print exception
        return parser.fanoutLink

    def GetPage(self, url):
        page = ''
        try:
            urlObject = urllib.urlopen(url, proxies = self.proxies)
            page = urlObject.read()
            urlObject.close()
        except Exception,exception:
            print exception
        return page

    def Run(self):
        curUrl = self.seedUrl
        urlQueue = Queue.Queue()
        urlQueue.put(curUrl)
        i = 0
        while urlQueue.empty() is not True and i < self.crawlPagesLimit:
            url = urlQueue.get();
            self.urlPages[url] = self.GetPage(url)
            #print self.urlPages[url]
            fanoutLink = self.GetFanoutLink(self.urlPages[url])
            for link in fanoutLink:
                urlQueue.put(link)
            i += 1

class CrawlingThread(Thread):
    crawler = UrlCrawler("http://www.qq.com", crawlPagesLimit = 1000)
    
    def run(self):
        self.crawler.Run()

