from HtmlParser import LinkExtractor

import time
import Queue
import urllib2
import threading

class UrlCrawler:
    urlPages = {}
    __initialize = False
    
    def __init__(self, parser = LinkExtractor(), proxies = {}, debug = False):
        self.__proxies = proxies
        self.__parser = parser
        self.__debug = debug
        proxy = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    def init(self, seedUrl = '', pagesLimit = 1000, crawlInterval = 0.01, timeout = 5):
        self.__seedUrl = seedUrl
        self.__pagesLimit = pagesLimit
        self.__crawlInterval = crawlInterval
        self.__timeout = timeout
        self.__initialize = True

    def print_params(self):
        print 'seed url is:', self.__seedUrl
        print 'crawl pages limit:', self.__pagesLimit
        print 'proxies:', self.__proxies
        print 'debug mode:', self.__debug
        print 'crawl interval', self.__crawlInterval
        print 'timeout for crawling single page', self.__timeout

    def parse(self, page):
        self.__parser.link.clear()
        try:
            self.__parser.feed(page)
        except Exception, exception:
            print exception
        return self.__parser.link

    def download(self, url):
        page = ''
        try:
            if self.__debug == True:
                print 'urlopen', url
            urlObject = urllib2.urlopen(url, timeout = self.__timeout)
            if self.__debug == True:
                print 'read url'
            page = urlObject.read()
            urlObject.close()
            if self.__debug == True:
                print 'finish reading'
        except Exception,exception:
            print exception
        return page

    def run(self):
        if self.__initialize == False:
            print 'Not initialize'
            return
        if self.__debug == True:
            self.print_params()
            print 'start running...'
        curUrl = self.__seedUrl
        urlQueue = Queue.Queue()
        urlQueue.put(curUrl)
        i = 0
        while urlQueue.empty() is not True and i < self.__pagesLimit:
            url = urlQueue.get();
            if self.__debug == True:
                print 'current crawling url is', url
            self.urlPages[url] = self.download(url)
            if self.__debug is True:
                print self.urlPages[url]
            link = self.parse(self.urlPages[url])
            for l in link:
                urlQueue.put(l)
            i += 1
            if self.__debug is True:
                print 'sleeping now...'
            time.sleep(self.__crawlInterval)

#from threading import Thread
#class CrawlingThread(Thread):
#    crawler = UrlCrawler("http://www.qq.com", pagesLimit = 1000)
#    
#    def run(self):
#        self.crawler.run()
#
