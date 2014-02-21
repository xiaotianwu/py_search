import sys
sys.path.append('../common')
from HtmlParser import LinkExtractor
from Common import UrlFileNameConverter

import re
import time
import Queue
import urllib2
import threading

# global chunk path
pageChunkPath = '../page_chunk/'
# global url chunk
urlChunk = set()
urlChunkLock = threading.RLock()

class UrlCrawler:
    urlPages = {}
    __initialize = False
    
    def __init__(self, proxies = {}, debug = False):
        self.__proxies = proxies
        self.___parser = LinkExtractor()
        self.__debug = debug
        proxy = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    def init(self, seedUrl, pagesLimit, crawlInterval, timeout, urlFilterRegexCollection):
        self.__seedUrl = seedUrl
        self.__pagesLimit = pagesLimit
        self.__crawlInterval = crawlInterval
        self.__timeout = timeout
        self.__initialize = True
        self.__urlFilterRegexCollection = urlFilterRegexCollection

    def print_params(self):
        print 'seed url is:', self.__seedUrl
        print 'crawl pages limit:', self.__pagesLimit
        print 'proxies:', self.__proxies
        print 'debug mode:', self.__debug
        print 'crawl interval', self.__crawlInterval
        print 'timeout for crawling single page', self.__timeout

    def _parse(self, page):
        self.___parser.link.clear()
        try:
            self.___parser.feed(page)
        except Exception, exception:
            print exception
            self.___parser.link.clear()
        return self.___parser.link

    def filter_url(self, url):
        for regex in self.__urlFilterRegexCollection:
            if regex.match(url):
                return True
        return False

    def _download(self, url):
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
            page = ''
        finally:
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
            url = urlQueue.get()
            url = url.strip(' /?') # delete the unuseful character in head/tail
            global urlChunk
            global urlChunkLock
            if url in urlChunk and url != self.__seedUrl:
                if self.__debug == True:
                    print 'url:', url, 'has been scanned' 
                    continue
            urlChunkLock.acquire()
            urlChunk.add(url)
            urlChunkLock.release()
            if self.__debug == True:
                print 'current crawling url is', url
            page = self._download(url)
            if page == '':
                if self.__debug == True:
                    print 'can not _download url', url
                continue
            # TODO make the file io async
            fileName = UrlFileNameConverter.url_to_filename(url)
            if self.__debug == True:
                print 'convert to file:', fileName
            global pageChunkPath
            pageFile = open(pageChunkPath + fileName, 'w');
            pageFile.write(page)
            pageFile.close()
            link = self._parse(page)
            for l in link:
                if l not in urlChunk and self.filter_url(l) is True:
                    urlQueue.put(l)
            self.urlPages[url] = page
            i += 1
            if self.__debug is True:
                print 'sleeping', self.__crawlInterval, 'second'
            time.sleep(self.__crawlInterval)

class UrlCrawlingThread(threading.Thread):
    def __init__(self, proxy = {}, debug = False):
        threading.Thread.__init__(self)
        self.__crawler = UrlCrawler(proxy, debug)

    def init(self, seedUrl, pagesLimit = 10, crawlInterval = 0.01, timeout = 5, urlFilterRegexCollection = [re.compile('.*')]):
        self.__crawler.init(seedUrl, pagesLimit, crawlInterval, timeout, urlFilterRegexCollection)

    def run(self):
        self.__crawler.run()
