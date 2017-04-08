import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
import sqlite3
ignorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:
    #initialize the crawler with the name of database
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)
    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()

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
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()
        