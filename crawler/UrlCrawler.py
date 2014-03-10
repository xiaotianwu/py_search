from multiprocessing.pool import ThreadPool
import os
import os.path
import Queue
import re
import threading
import time
import urllib2

from common.HtmlParser import LinkExtractor
from common.Logger import Logger
from UrlDumper import UrlDumper

class UrlCrawler:
    __seedUrl = None
    __downloadPath = None
    __proxies = None
    __globalInit = False
    __globalLock = threading.RLock()
    __urlQueue = Queue.Queue()
    __urlChunk = set()
    __urlChunkLock = threading.RLock()
    __urlDumperThreads = ThreadPool(4)
   
    @staticmethod
    def GlobalInit(seedUrl, downloadPath, proxies = {}):
        '''called at first in the program'''
        UrlCrawler.__globalLock.acquire()

        if UrlCrawler.__globalInit == True:
            UrlCrawler.__globalLock.release()
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
        UrlDumper.Init(downloadPath, 'url_and_page')
        UrlCrawler.__globalInit = True

        UrlCrawler.__globalLock.release()

    @staticmethod
    def GlobalExit():
        '''in order to quit dumper thread safely'''
        UrlCrawler.__urlDumperThreads.close()
        UrlCrawler.__urlDumperThreads.join()

    def __init__(self):
        self._init = False
        self._logger = Logger.Get('UrlCrawler')
        self._parser = LinkExtractor()

    def Init(self, pagesLimit, crawlInterval,
             timeout, urlFilterRegexCollection):
        self._pagesLimit = pagesLimit
        self._crawlInterval = crawlInterval
        self._timeout = timeout
        self._urlFilterRegexCollection = urlFilterRegexCollection
        self._init = True

    def PrintParams(self):
        self._logger.info('seed url: '+ UrlCrawler.__seedUrl)
        self._logger.info('proxies: ' + str(UrlCrawler.__proxies))
        self._logger.info('crawl pages limit: '+ str(self._pagesLimit))
        self._logger.info('crawl interval: '+ str(self._crawlInterval))
        self._logger.info('crawl timeout: '+ str(self._timeout))
        self._logger.info('parser type: ' + str(type(self._parser)))

    def _Parse(self, page):
        self._parser.link.clear()
        try:
            self._parser.feed(page)
        except Exception as exception:
            print exception
        finally:
            self._parser.close()
        return self._parser.link

    def _FilterUrl(self, url):
        if self._urlFilterRegexCollection == None:
            return True
        for regex in self._urlFilterRegexCollection:
            if regex.match(url):
                return True
        return False

    def _Download(self, url):
        page = None
        try:
            self._logger.info('urlopen ' + url)
            urlObject = urllib2.urlopen(url, timeout = self._timeout)
            self._logger.info('read url ' + url)
            page = urlObject.read()
            urlObject.close()
            self._logger.info('finish reading ' + url)
        except Exception as exception:
            print exception
            page = None
        finally:
            return page

    def _ConvertToLegalUrl(self, homepage, url):
        if url.startswith('http://'):
            return url
        elif url.startswith('./'):
            return homepage + url[1:]
        else:
            return None

    def Run(self):
        if UrlCrawler.__globalInit == False or self._init == False:
            raise Exception('call GlobalInit before start crawling')
        self.PrintParams()
        self._logger.info('start crawling...')

        i = 0
        while i < self._pagesLimit:
            url = UrlCrawler.__urlQueue.get(timeout = 60)
            if url == None:
                break 
            url = url.strip(' /?')

            UrlCrawler.__urlChunkLock.acquire()
            if url in UrlCrawler.__urlChunk:
                self._logger.info('url: ' + url + ' has been scanned, skip it')
                continue
            UrlCrawler.__urlChunk.add(url)
            UrlCrawler.__urlChunkLock.release()

            self._logger.info('current downloading: ' + url)
            page = self._Download(url)
            if page == None:
                self._logger.info('can not download: ' + url)
                continue

            linkList = self._Parse(page)
            self._logger.info('get ' + len(linkList) + ' links')
            for link in linkList:
                if (link is not None and
                    link not in UrlCrawler.__urlChunk and
                    self._FilterUrl(link) == True):
                    UrlCrawler.__urlQueue.put(link)
            dumpThreads = UrlCrawler.__urlDumperThreads
            dumpThreads.apply_async(UrlDumper.Write, (url, page))

            i += 1
            self._logger.info('sleep ' + str(self._crawlInterval) + ' seconds')
            time.sleep(self._crawlInterval)

        self._logger.info('crawler terminated')


    def GetUrlChunk(self):
        return UrlCrawler.__urlChunk

class UrlCrawlingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._crawler = UrlCrawler()

    def Init(self, pagesLimit = 10,
             crawlInterval = 1, timeout = 5,
             urlFilterRegexCollection = [re.compile('.*')]):
        self._crawler.Init(pagesLimit, crawlInterval,
                           timeout, urlFilterRegexCollection)

    def run(self):
        self._crawler.Run()
