import re

from HTMLParser import HTMLParser

class ExtendedHTMLParser(HTMLParser):
    fanoutLink = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 0:
               pass
            else:
               for (name, value) in attrs:
                   # print (name, value)
                   if name == 'href':
                       self.fanoutLink.append(value)
