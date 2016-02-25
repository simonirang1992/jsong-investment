from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
import sys
from logger import writelog
import http.client

# Initialize
def yql_highlight_init():
	cn = getconf('highlight')
	if not cn:
		p = []
		writelog('[CRITICAL] No Configuration File Found', 'yql_highlight_init', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	d = 'DROP TABLE IF EXISTS yql_highlight'
	dberase(d)

	s = 'CREATE TABLE yql_highlight (id INT NOT NULL AUTO_INCREMENT, tick VARCHAR(10), '
	for ele in cn:
		s = s + ele + ' VARCHAR(15), '
	s = s[:-2] + ', PRIMARY KEY(id))'
	dbquery(s)
	return 0

# Collects Beta
def yql_highlight(tick, attempts):
    # Web Scrapping
	p = []
	p.append(tick)
	p.append(attempts)
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
	
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_highlight', p)
		writelog(e, 'yql_highlight', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_highlight', p)
		writelog(e, 'yql_highlight', p)
		return 1
	except http.client.IncompleteRead as e:
                writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_highlight', p)
                if (attempts < 3):
                        r =yql_highlight(tick, attempts + 1)
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_highlight', p)
                        return 1

                if (r == 0):
                        return 0
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_highlight', p)
                        return 1

	# Remove subscripts
	for tag in soup.find_all('sup'):
		tag.replaceWith('')

	table = soup.find_all("table", { "class" : "yfnc_datamodoutline1" })

	cn = getconf('highlight')
	if not cn:
		p = []
		writelog('[CRITICAL] No Configuration File Found', 'yql_highlight', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1

	d = 'DELETE FROM yql_highlight WHERE tick = \'' + tick + '\''
	dbquery(d)

	s = 'INSERT INTO yql_highlight (tick, '
	for ele in cn:
		s = s + ele + ', '
	s = s[:-2] + ') VALUES (\'' + tick + '\', '


	i = 0
	ccl = []
	try:
		for ele in table: #.findAll("table"):
			if (i >= 1) and (i <= 4):
				for row in ele.findAll("tr"):
					if len(row) == 2:
						for col in row.findAll("td"):
							if (col.get_text().find(':') == -1):
								#print (col.get_text())
								g = col.get_text()
								g = g.replace(' ', '')
								g = g.replace('%', '')
								ccl.append(g)
								#s = s + '\"' + g + '\"' + ', '
			i = i + 1
		#s = s[:-2] + ')'
	except IndexError as e:
		writelog('[WARNING] INDEX ERROR Encountered ' + str(e), 'yql_highlight', p)
		return 1
	
	if (len(ccl) == len(cn)):
		for cc in ccl:
			s = s + '\"' + cc + '\"' + ', '
		s = s[:-2] + ')'
		dbquery(s)
		return 0
	else:
		writelog('[CRITICAL] No Data Retrieved', 'yql_highlight', p)
		return 1
