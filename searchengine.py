import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin

ignorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:
    #initialize the crawler with the name of database
    def __init__(self,dbname):
        pass
    def __del__(self):
        pass
    def dbcommit(self):
        pass

    def getentryid(self, table, field, value, createnew=True):
        return None

    def addtoindex(self, url, soup):
        print('index {}'.format(url))

    def gettextonly(self, soup):
        return None

    def separaterwords(self, text):
        return None

    def isindexed(self,url):
         return False

    def addlinkref(self, urlfrom, urlto, linkltext):
        pass

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib.request.urlopen(page)
                except:
                    print('Could not open {}'.format(page))
                    continue
                soup=BeautifulSoup(c.read(),'lxml')
                self.addtoindex(page, soup)

                links=soup('a')
                for link in links:
                    print(link.attrs)
                    if 'href' in dict(link.attrs):
                        url=urljoin(page, link['href'])
                        if url.find("'")!=-1:
                            continue
                        url=url.split('#')[0]
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linktext=self.gettextonly(link)
                        self.addlinkref(page, url, linktext)
                self.dbcommit()
            pages=newpages



    def createindextables(self):
        pass

sourcepage=['http://www.6park.com/sg.shtml']
cw=crawler('')
cw.crawl(pages=sourcepage)
