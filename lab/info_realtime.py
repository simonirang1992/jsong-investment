
__author__ = 'ssong'
from bs4 import BeautifulSoup
from config import getconf
import pymysql
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Real time for evertything
def info_real_populate():
    p = []
    conn = pymysql.connect(host='localhost',port=3306, user='jsong', passwd='password', db='jsong')
    cur = conn.cursor()
    cur.execute("SELECT tick, errorfnc FROM ticklist") #WHERE (errorfnc is NULL or errorfnc = \"\")")
    msg = '0'
    count = 1
    #for tick in cname:
    ticklist = ""
    tickstore = []
    c = 0
    for tick1 in cur.fetchall():
        tick = tick1[0]
        if c == 1500:
            c = 0
            tickstore.append(ticklist[:-1])
            break
            ticklist = ""
        ticklist = ticklist + tick + "+"
        c = c + 1
    print (str(c))
    #tickstore.append(ticklist[:-1])
    cur.close()
    conn.close()
    for ticklist in tickstore:
        req = Request(
           'http://finance.yahoo.com/d/quotes.csv?s=' + ticklist + '&f=sbb2b3c6ej3m2r2j1',
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
    htmlx = urlopen(req)
    data = htmlx.read()
    soup = BeautifulSoup(data, 'html.parser')
    print (soup)
    return 0

info_real_populate()
