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
        cur=self.con.execute("select rowid from {} where {}=:value".format(table, field),{"value":value})
        res=cur.fetchone()
        if res==None:
            cur=self.con.executemany("insert into {} ({}) :values".format(table, field),{"value":value})
            return cur.lastrowid
        else:
            return res[0]


    def addtoindex(self, url, soup):
        if self.isindexed(url):return ''
        print('indexing '+url)

        text=self.gettextonly(soup)
        words=self.separaterwords(text)

        urlid=self.getentryid('urllist', 'url', url)

        for i in range(len(words)):
            word=words[i]
            if word in ignorewords:continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid, wordid, location) values (?,?,?),(urlid, wordid,i)")


    def gettextonly(self, soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttxt=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttxt+=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    def separaterwords(self, text):
        splitter=re.compile('\\W*')
        return [s.lower for s in splitter.split(text) if s!='']

    def isindexed(self,url):
        u=self.con.execute("select rowid from urllist where url=?",(url)).fetchone()
        print(u)
        if u!= None :
            v=self.con.execute("select * from wordlocation where urlid=?",(u[0])).fetchone()
            if v!=None: return True
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
        