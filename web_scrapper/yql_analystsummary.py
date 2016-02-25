from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
import sys
from logger import writelog
import http.client

# Initialize
def yql_analyst_summary_init():
	cn = getconf('analyst_summary')
	if not cn:
		p = []
		writelog('[CRITICAL] No Configuration File Found', 'yql_analyst_summary_init', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	d = 'DROP TABLE IF EXISTS yql_analyst_summary'
	dberase(d)
	
	s = 'CREATE TABLE yql_analyst_summary (id INT NOT NULL AUTO_INCREMENT, tick VARCHAR(15), '
	for ele in cn:
		s = s + ele + ' VARCHAR(15), '
	s = s[:-2] + ', PRIMARY KEY(id))'
	dbquery(s)
	return 0

# Collects Beta
def yql_analyst_summary(tick,attempts):
	p = []
	p.append(tick)
	p.append(attempts)
    # Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/q/ao?s=' + tick + '+Analyst+Opinion',
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

		table = soup.find_all("table", { "class" : "yfnc_datamodoutline1 equaltable" })
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered' + str(e), 'yql_analyst_summary', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered ' + str(e), 'yql_analyst_summary', p)
		return 1
	except http.client.IncompleteRead as e:
		writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_analyst_summary', p)
		if (attempts < 3):
			r = yql_analyst_summary(tick, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_analyst_summary', p)	
			return 1

		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_analyst_summary', p)
			return 1


	d = 'DELETE FROM yql_analyst_summary WHERE tick = ' + '\'' + tick + '\''
	dbquery(d)

	cn = getconf('analyst_summary')
	if not cn:
		writelog('[CRITICAL] No Configuration File Found', 'yql_analyst_summary', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1

	s = 'INSERT INTO yql_analyst_summary (tick, '
	for ele in cn:
		s = s + ele + ', '
	s = s[:-2] + ') VALUES (\'' + tick + '\', '
	ccl = []
	for ele in table:
		for row in ele.findAll("tr"):
			for col in row.findAll("td"):
				if (col.get_text().find(':') == -1):
					ts = col.get_text()
					ts = ts.replace("%","")
					ccl.append(ts)	
	
	if (len(ccl) == len(cn)):
		for cc in ccl:
			s = s + '\'' + cc + '\', '
		s = s[:-2] + ')'
		dbquery(s)
		return 0
	else:
		return 1
