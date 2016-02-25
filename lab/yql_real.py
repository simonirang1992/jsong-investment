from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
from logger import writelog
import datetime
import http.client
def yql_real_init():
	# Drop Table if exists
	d = 'DROP TABLE IF EXISTS yql_real'
	dberase(d)
	# Creating new table
	s = 'CREATE TABLE yql_real (id INT NOT NULL AUTO_INCREMENT, tick VARCHAR(10), ask VARCHAR(10), bid VARCHAR(10), rchange VARCHAR(10), es VARCHAR(10), marketcap VARCHAR(20), dayr VARCHAR(10), pe VARCHAR(10), smc VARCHAR(20), PRIMARY KEY (id))'
	dbquery(s)
	return 0

def yql_real(tick, attempts):
	p = []
	p.append(tick)
	p.append(attempts)
    # Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/d/quotes.csv?s=' + tick + '&f=b2b3c6ej3m2r2j1',
			data=None,
			headers={
				   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
		html = urlopen(req)
		data = html.read()

	        # Parsing
		soup = BeautifulSoup(data, 'html.parser')
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered' + str(e), 'yql_real', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered ' + str(e), 'yql_real', p)
		return 1
	except http.client.IncompleteRead as e:
                writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_real', p)
                if (attempts < 3):
                        r = yql_growth(tick, attempts + 1)
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_real', p)
                        return 1

                if (r == 0):
                        return 0
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_real', p)
                        return 1
	
	# Remove subscripts
	for tag in soup.find_all('sup'):
		tag.replaceWith('')
	
	soup = str(soup)
	ts = soup.split(',')
	
	# Delete Row
	dquery = 'DELETE FROM yql_real WHERE tick = \'' + tick + '\''
	dbquery(dquery)

	# Insert Row
	iquery = 'INSERT INTO yql_real (tick, ask, bid, rchange, es, marketcap, dayr, pe, smc) VALUES (\'' + tick + '\','
	for ele in ts:
		iquery = iquery + '\'' + ele + '\', '
	iquery = iquery[:-2] + ')'
	dbquery(iquery)
	return 0
