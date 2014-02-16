import os
import os.path
import Queue
import re
import sys
import threading
import time
import urllib2
sys.path.append('../common')

from HtmlParser import LinkExtractor
from Common import UrlFileNameConverter

# global chunk path
pageChunkPath = '../page_chunk/'
# global url chunk
urlChunk = set()
urlChunkLock = threading.RLock()

class UrlCrawler:
    __proxies = None
    __downloadPath = None
    __global_init = False
    __global_lock = threading.RLock()

    # _init only once in the program
    @staticmethod
    def global_init(downloadPath = pageChunkPath,
                    proxies = {},
                    parser = LinkExtractor()):
        UrlCrawler.__global_lock.acquire()
        if UrlCrawler.__global_init is True:
            UrlCrawler.__global_lock.release()
            return
        UrlCrawler.__proxies = proxies
        proxy = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        if not os.path.exists(downloadPath):
            os.mkdir(downloadPath)
        UrlCrawler.__downloadPath = downloadPath
        UrlCrawler.__global_init = True
        UrlCrawler.__global_lock.release()

    def __init__(self, debug = False):
        self._urlPages = {}
        self._init = False
        self._debug = debug

    def init(self, seedUrl, pagesLimit,
             crawlInterval, timeout, urlFilterRegexCollection,
             parser = LinkExtractor()):
        self._seedUrl = seedUrl
        self._pagesLimit = pagesLimit
        self._crawlInterval = crawlInterval
        self._timeout = timeout
        self._urlFilterRegexCollection = urlFilterRegexCollection
        self._parser = parser
        self._init = True
        self._path = UrlCrawler.__downloadPath

    # only affect the current crawler instance
    def change_download_path(self, path):
        self._path = path

    def print_params(self):
        print 'seed url is:', self._seedUrl
        print 'crawl pages limit:', self._pagesLimit
        print 'proxies:', self.__proxies
        print 'debug mode:', self._debug
        print 'crawl interval', self._crawlInterval
        print 'timeout for crawling single page', self._timeout
        print 'parser type is', type(self._parser)

    def _parse(self, page):
        self._parser.link.clear()
        try:
            self._parser.feed(page)
        except Exception, exception:
            print exception
        finally:
            self._parser.close()
        return self._parser.link

    def _filter_url(self, url):
        for regex in self._urlFilterRegexCollection:
            if regex.match(url):
                return True
        return False

    def _download(self, url):
        page = None
        try:
            if self._debug == True:
                print 'urlopen', url
            urlObject = urllib2.urlopen(url, timeout = self._timeout)
            if self._debug == True:
                print 'read url'
            page = urlObject.read()
            urlObject.close()
            if self._debug == True:
                print 'finish reading'
        except Exception,exception:
            print exception
            page = None
        finally:
            return page

    def _convert_to_legal_url(self, homepage, url):
        if url.startswith('http://'):
            return url
        elif url.startswith('./'):
            return homepage + url[1:]
        else:
            return None

    def run(self):
        if UrlCrawler.__global_init == False or self._init == False:
            print 'Not init'
            return
        if self._debug == True:
            self.print_params()
            print 'start running...'
        curUrl = self._seedUrl
        urlQueue = Queue.Queue()
        urlQueue.put(curUrl)
        i = 0
        while urlQueue.empty() is not True and i < self._pagesLimit:
            url = urlQueue.get()
            # delete the unuseful character in head/tail
            url = url.strip(' /?')
            global urlChunk
            global urlChunkLock
            if url in urlChunk and url != self._seedUrl:
                if self._debug == True:
                    print 'url:', url, 'has been scanned' 
                    continue
            urlChunkLock.acquire()
            urlChunk.add(url)
            urlChunkLock.release()
            if self._debug == True:
                print 'current crawling url is', url
            page = self._download(url)
            if page == None:
                if self._debug == True:
                    print 'can not download url', url
                continue
            # TODO make the file io async
            fileName = UrlFileNameConverter.url_to_filename(url)
            if self._debug == True:
                print 'convert to file:', fileName
            pageFile = open(self._path + fileName, 'w');
            pageFile.write(page)
            pageFile.close()
            link = self._parse(page)
            for l in link:
                if (l is not None and l not in urlChunk and
                       self._filter_url(l) is True):
                    urlQueue.put(l)
            self._urlPages[url] = page
            i += 1
            if self._debug is True:
                print 'sleeping', self._crawlInterval, 'second'
            time.sleep(self._crawlInterval)

class UrlCrawlingThread(threading.Thread):
    def __init__(self, proxy = {}, debug = False):
        threading.Thread.__init__(self)
        self._crawler = UrlCrawler(debug)

    def init(self, seedUrl, pagesLimit = 10, crawlInterval = 0.01,
             timeout = 5, urlFilterRegexCollection = [re.compile('.*')]):
        self._crawler.init(seedUrl, pagesLimit, crawlInterval,
                           timeout, urlFilterRegexCollection)

    def run(self):
        self._crawler.run()
