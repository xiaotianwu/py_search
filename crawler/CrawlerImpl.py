from HtmlParser import LinkExtractor

import time
import Queue
import urllib2
import threading

# global chunk path
pageChunkPath = './page_chunk/'
# global url chunk
urlChunk = set()
urlChunkLock = threading.RLock()

class UrlFileNameConverter:
    @staticmethod
    def url_to_filename(url):
        return url.replace('/', '^')

    @staticmethod
    def filename_to_url(fileName):
        return fileName.replace('^', '/')

class UrlCrawler:
    urlPages = {}
    __initialize = False
    
    def __init__(self, proxies, debug):
        self.__proxies = proxies
        self.__parser = LinkExtractor()
        self.__debug = debug
        proxy = urllib2.ProxyHandler(proxies)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

    def init(self, seedUrl, pagesLimit, crawlInterval, timeout):
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
            url = urlQueue.get();
            global urlChunk
            global urlChunkLock
            if url in urlChunk:
                if self.__debug == True:
                    print 'url:', url, 'has been scanned' 
                    continue
            urlChunkLock.acquire()
            urlChunk.add(url)
            urlChunkLock.release()
            if self.__debug == True:
                print 'current crawling url is', url
            page = self.download(url)
            if page == '':
                if self.__debug == True:
                    print 'can not download url', url
                continue
            # make the file io async
            fileName = UrlFileNameConverter.url_to_filename(url)
            if self.__debug == True:
                print 'convert to file:', fileName
            global pageChunkPath
            pageFile = open(pageChunkPath + fileName, 'w');
            pageFile.write(page)
            pageFile.close()
            link = self.parse(page)
            for l in link:
                if l not in urlChunk:
                    urlQueue.put(l)
            self.urlPages[url] = page
            i += 1
            if self.__debug is True:
                print 'sleeping now...'
            time.sleep(self.__crawlInterval)

class UrlCrawlingThread(threading.Thread):
    def __init__(self, proxy = {}, debugOpen = False):
        threading.Thread.__init__(self)
        self.__crawler = UrlCrawler(proxies = proxy, debug = debugOpen)

    def init(self, seedUrl, pagesLimit = 10, crawlInterval = 0.01, timeout = 5):
        self.__crawler.init(seedUrl, pagesLimit, crawlInterval, timeout)

    def run(self):
        self.__crawler.run()
