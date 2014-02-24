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
    __seedUrl = None
    # class Queue is thread-safe, and it's a
    # unique queue shared with all crawler
    __urlQueue = Queue.Queue()
   
    # _init only once in the program
    @staticmethod
    def global_init(seedUrl,
                    downloadPath = pageChunkPath,
                    proxies = {}):
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
        UrlCrawler.__seedUrl = seedUrl
        UrlCrawler.__urlQueue.put(seedUrl)
        UrlCrawler.__global_init = True
        UrlCrawler.__global_lock.release()

    def __init__(self, debug = False):
        self._urlPages = {}
        self._init = False
        self._debug = debug

    def init(self, crawlerId, pagesLimit, crawlInterval,
             timeout, urlFilterRegexCollection, parser):
        self._pagesLimit = pagesLimit
        self._crawlInterval = crawlInterval
        self._timeout = timeout
        self._urlFilterRegexCollection = urlFilterRegexCollection
        self._parser = parser
        self._path = UrlCrawler.__downloadPath
        self._init = True
        self._crawlerId = crawlerId

    def print_params(self):
        print 'seed url:', UrlCrawler.__seedUrl
        print 'crawl pages limit:', self._pagesLimit
        print 'proxies:', self.__proxies
        print 'debug mode:', self._debug
        print 'crawl interval', self._crawlInterval
        print 'timeout for crawling single page', self._timeout
        print 'parser type is', type(self._parser)

    def set_download_path(self, path):
        self._path = path

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
                print 'Crawler', self._crawlerId, 'urlopen', url
            urlObject = urllib2.urlopen(url, timeout = self._timeout)
            if self._debug == True:
                print 'Crawler', self._crawlerId, 'read url'
            page = urlObject.read()
            urlObject.close()
            if self._debug == True:
                print 'Crawler', self._crawlerId, 'finish reading'
        except Exception, exception:
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
            print 'Crawler', self._crawlerId, 'Not init'
            return
        if self._debug == True:
            self.print_params()
            print 'Crawler', self._crawlerId, 'start running...'
        i = 0
        while i < self._pagesLimit:
            have_sleep = False
            while UrlCrawler.__urlQueue.empty() == True:
                if have_sleep == True:
                    return
                time.sleep(20)
                # sleeping only once
                have_sleep = True;
            else:                    
                url = UrlCrawler.__urlQueue.get()
            # double check
            if url == None:
                return
            # delete the unuseful character in head/tail
            url = url.strip(' /?')
            global urlChunk
            global urlChunkLock
            urlChunkLock.acquire()
            if url in urlChunk:
                if self._debug == True:
                    print 'Crawler', self._crawlerId,\
                          'url:', url, 'has been scanned' 
                    continue
            urlChunk.add(url)
            urlChunkLock.release()
            if self._debug == True:
                print 'Crawler', self._crawlerId, 'current crawling url is', url
            page = self._download(url)
            if page == None:
                if self._debug == True:
                    print 'Crawler', self._crawlerId,\
                          'can not download url', url
                continue
            # TODO make the file io async
            fileName = UrlFileNameConverter.url_to_filename(url)
            if self._debug == True:
                print 'Crawler', self._crawlerId, 'convert to file:', fileName
            with open(self._path + fileName, 'w') as pageFile:
                pageFile.write(page)
            link = self._parse(page)
            for l in link:
                if (l is not None and l not in urlChunk and
                       self._filter_url(l) is True):
                    UrlCrawler.__urlQueue.put(l)
            self._urlPages[url] = page
            i += 1
            if self._debug is True:
                print 'Crawler', self._crawlerId, 'sleeping',\
                      self._crawlInterval, 'second'
            time.sleep(self._crawlInterval)

class UrlCrawlingThread(threading.Thread):
    def __init__(self, debug = False):
        threading.Thread.__init__(self)
        self._crawler = UrlCrawler(debug)

    def init(self, crawlerId, pagesLimit = 10,
             crawlInterval = 1, timeout = 5,
             urlFilterRegexCollection = [re.compile('.*')],
             parser = LinkExtractor()):
        self._crawler.init(crawlerId, pagesLimit, crawlInterval, timeout,
                           urlFilterRegexCollection, parser)

    def run(self):
        self._crawler.run()
