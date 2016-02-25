from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
import re
import sys
from logger import writelog
import http.client
# Initialize
def yql_day_init():
	cn = getconf('day')
	if not cn:
		p = []
		writelog('[CRITICAL] No Configuration File Found', 'yql_day_init', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	d = 'DROP TABLE IF EXISTS yql_day'
	dberase(d)


	s = 'CREATE TABLE yql_day (id INT NOT NULL AUTO_INCREMENT, tick VARCHAR(10), '
	for ele in cn:
		s = s + ele + ' VARCHAR(15), '
	s = s[:-2] + ', PRIMARY KEY(id))'
	dbquery(s)
	return 0


# Collects Beta
def yql_beta(tick, attempts):
	p = []
	p.append(tick)
	p.append(attempts)
        # Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/q/ks?s=' + tick + '+Key+Statistics',
			data=None,
			headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
			}
		)
		html = urlopen(req)
		data = html.read()

		# Find table & Parse
		soup = BeautifulSoup(data, 'html.parser')
		for tag in soup.find_all('sup'):
			tag.replaceWith('')
		table = soup.findAll("table", { "class" : "yfnc_datamodoutline1" })
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_beta', p)
		writelog(e, 'yql_beta', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_beta', p)
		writelog(e, 'yql_beta', p)
		return 1
	except http.client.IncompleteRead as e:
		writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_beta', p)
		if (attempts < 3):
			r = yql_beta(tick, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_beta', p)	
			return 1

		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_beta', p)
			return 1

	beta = False
	next = False
	try:
		for ele in table:
			for row in ele.findAll("tr"):
				for col in row.findAll("td"):
					if next == True:
						beta = True
						return (str(col.get_text()))
					if re.match("^Beta:", col.get_text()):
						next = True
	except IndexError as e:
		p = []
		p.append(tick)
		writelog('[WARNING] INDEX ERROR Encountered', 'yql_beta', p)
		writelog(e, 'yql_beta', p)
		return 1
	return 1

def yql_day(tick, attempts):
    # Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/d/quotes.csv?s=' + tick + '&f=a2dghj4vxy',
			data=None,
			headers={
				   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
		html = urlopen(req)
		data = html.read()
	except URLError as e:
		p = []
		p.append(tick)
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_day', p)
		writelog(e, 'yql_day', p)
		sys.exit('[CRITICAL] URL ERROR')
	except HTTPError as e:
		p = []
		p.append(tick)
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_day', p)
		writelog(e, 'yql_day', p)
		return 1
    # Parse
	soup = BeautifulSoup(data, 'html.parser')
	for tag in soup.find_all('sup'):
		tag.replaceWith('')

	soup = str(soup)
	ts = soup.split(',')

	# Erase Table	
	dquery = 'DELETE FROM yql_day WHERE tick = ' + '\'' + tick + '\''
	dbquery(dquery)

	iquery = 'INSERT INTO yql_day (tick, '
	cn = getconf('day')
	if not cn:
		p = []
		writelog('[CRITICAL] No Configuration File Found', 'yql_day', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	for ele in cn:
		iquery = iquery + ele + ', '
	iquery = iquery[:-2] + ') VALUES (\'' + tick + '\', '

	if (len(cn) == len(ts) + 1):
		for el in ts:
			el = el.replace("\n","")
			el = el.replace('\"','')
			el = el.replace("\\","")
			iquery = iquery + '\'' + el + '\', '
	else:
		return 1
	beta = yql_beta(tick, 0)
	
	if beta == 0:
		beta = 'NA'
		p = []
		p.append(tick)
		writelog('Unable to collect beta', 'yql_day', p)

	iquery = iquery + '\'' + str(beta) + '\')'
	#iquery = iquery[:-3] + ')'
	dbquery(iquery)
	#print (iquery)
	return 0

