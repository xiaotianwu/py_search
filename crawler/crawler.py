import re
import Queue
import urllib
import threading
from HTMLParser import HTMLParser
from threading import Thread

class ExtendedHTMLParser(HTMLParser):
    fanout_link = []
    http_regex = re.compile("http://*")

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if len(attr) == 2 and \
               attr[0] == 'href' and \
               self.http_regex.match(attr[1]):
                print "href:", attr[1]
                self.fanout_link.append(attr[1])

class UrlCrawler:
    seed_url = ''
    crawl_pages_limit = 0
    proxies = {}
    url_pages = {}
    
    def __init__(self, seed_url, crawl_pages_limit = 10, proxies = {}):
        self.seed_url = seed_url
        self.crawl_pages_limit = crawl_pages_limit
        self.proxies = proxies

    def GetFanoutLink(self, page_text):
        parser = ExtendedHTMLParser()
        try:
            parser.feed(page_text)
        except Exception, exception:
            print exception
        return parser.fanout_link

    def GetPage(self, url):
        page = ''
        try:
            url_object = urllib.urlopen(url, proxies = self.proxies)
            page = url_object.read()
            url_object.close()
        except Exception,exception:
            print exception
        return page

    def Run(self):
        current_url = self.seed_url
        url_queue = Queue.Queue()
        url_queue.put(current_url)
        i = 0
        while url_queue.empty() is not True and i < self.crawl_pages_limit:
            url = url_queue.get();
            self.url_pages[url] = self.GetPage(url)
            #print self.url_pages[url]
            fanout_link = self.GetFanoutLink(self.url_pages[url])
            for link in fanout_link:
                url_queue.put(link)
            i += 1

class CrawlingThread(Thread):
    crawler = UrlCrawler("http://www.qq.com", crawl_pages_limit = 1000)
    
    def run(self):
        self.crawler.Run()

for i in range(1, 5):
    crawling_thread = CrawlingThread();
    crawling_thread.start()

#parser = ExtendedHTMLParser();
#parser.feed(open('c:\\python27\\test.html','r').read())

#crawler = UrlCrawler("http://www.qq.com", crawl_pages_limit = 1000)
#crawler.Run()
#for key in crawler.url_pages.keys():
#    print key
#print crawler.GetPage("http://www.qqq.com")