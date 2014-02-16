from HTMLParser import HTMLParser

import Queue
import urllib
import threading
from threading import Thread

class UrlCrawler:
    urlPages = {}
    
    def __init__(self, seedUrl = '', parser = ExtendedHTMLParser(), crawlLimit = 10, proxies = {}, debug = False):
        self.__seedUrl = seedUrl
        self.__crawlLimit = crawlLimit
        self.__proxies = proxies
        self.__parser = parser
        self.__debug = debug

    def print_params(self):
        print 'seed url is:', self.__seedUrl
        print 'crawl level limits:', self.__crawlLimit
        print 'proxies:', self.__proxies
        print 'stop words:', self.__parser.stopwords
        print 'debug mode:', self.__debug
        print 'wordbreaker type:', self.__parser.wordBreaker.type_name

    def parse(self, page):
        self.__parser.clear_parse_result()
        try:
            self.__parser.feed(page)
        except Exception, exception:
            print exception

    def download(self, url):
        page = ''
        try:
            urlObject = urllib.urlopen(url, proxies = self.__proxies)
            page = urlObject.read()
            urlObject.close()
        except Exception,exception:
            print exception
        return page

    def run(self):
        curUrl = self.__seedUrl
        urlQueue = Queue.Queue()
        urlQueue.put(curUrl)
        i = 0
        while urlQueue.empty() is not True and i < self.__crawlLimit:
            url = urlQueue.get();
            self.urlPages[url] = self.download(url)
            if self.__debug is True:
                print self.urlPages[url]
            finishedParser = self.parse(self.urlPages[url])
            for l in finishedParser.link:
                urlQueue.put(l)
            i += 1

class CrawlingThread(Thread):
    crawler = UrlCrawler("http://www.qq.com", __crawlLimit = 1000)
    
    def run(self):
        self.crawler.run()

