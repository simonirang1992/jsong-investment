from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
import sys
from logger import writelog
import http.client

# Initialize
def yql_competitor_init(tick):
	cn = getconf('competitor')
	if not cn:
		p = []
		p.append(tick)
		writelog('[CRITICAL] No Configuration File Found', 'yql_competitor_init', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	d = 'DROP TABLE IF EXISTS ' + tick + '_yql_competitor'
	dberase(d)
	
	s = 'CREATE TABLE ' + tick + '_yql_competitor (id INT NOT NULL AUTO_INCREMENT, tick VARCHAR(15), '
	for ele in cn:
		s = s + ele + ' VARCHAR(15), '
	s = s[:-2] + ', PRIMARY KEY(id))'
	#print (s)
	dbquery(s)
	return 0

# Collects Beta
def yql_competitor(tick, attempts):
	p = []
	p.append(tick)
	p.append(attempts)
	# Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/q/co?s=' + tick + '+Competitors',
			data=None,
			headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
			}
		)
		html = urlopen(req)
		data = html.read()

		# Find table & Parse
		soup = BeautifulSoup(data, 'html.parser')
		
		# Remove subscripts
		for tag in soup.find_all('sup'):
			tag.replaceWith('')

		table = soup.find_all("table", { "class" : "yfnc_datamodoutline1" })
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_competitor', p)
		writelog(e, 'yql_competitor', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_competitor', p)
		writelog(e, 'yql_competitor', p)
		return 1
	except http.client.IncompleteRead as e:
		writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_competitor', p)
		if (attempts < 3):
			r = yql_competitor(tick, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_competitor', p)	
			return 1

		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_competitor', p)
			return 1



	cl = []
	first = True
	try:
		for ele in table:
			for row in ele.findAll("tr"):
				if (first == True):
					for col in row.findAll("th"):
						cn = []
						if (first == True):
							first = False
						elif (col.get_text().find(':') > -1):
							break
						else:
							cn.append(col.get_text())
							cl.append(cn)
				else:
					i = 0
					for col in row.findAll("td"):
						cl[i].append(col.get_text())
						i = i + 1
			break
	except IndexError as e:
		writelog('[WARNING] INDEX ERROR Encountered', 'yql_competitor', p)
		writelog(e, 'yql_competitor', p)
		return 1

	s = 'INSERT INTO ' + tick + '_yql_competitor (tick, '
	cn = getconf('competitor')
	if not cn:
		writelog('[CRITICAL] No Configuration File Found', 'yql_competitors', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	for ele in cn:
		s = s + ele + ', '
	s = s[:-2] + ') VALUES ('

	retval = 0

	for col in cl:
		gs = s
		if (len(cn) == len(col) - 1):
			for row in col:
				gs = gs + '\'' + str(row) + '\', ' 
			gs = gs[:-2] + ')'
			dbquery(gs)
		else:
			retval = 1
	return retval
