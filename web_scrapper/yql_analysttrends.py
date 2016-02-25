from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
import sys
from logger import writelog
import http.client

# Initialize
def yql_analyst_trends_init(tick):
	d = 'DROP TABLE IF EXISTS ' + tick + '_yql_analyst_trends'
	dberase(d)

	s = 'CREATE TABLE ' + tick + '_yql_analyst_trends (id INT NOT NULL AUTO_INCREMENT, Strong_Buy VARCHAR(10), Buy VARCHAR(10), Hold VARCHAR(10), Underperform VARCHAR(10), Sell VARCHAR(10), PRIMARY KEY(id))'
	dbquery(s)
	return 0

# Collects Beta
def yql_analyst_trends(tick,attempts):
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
		table = soup.find_all("table", { "class" : "yfnc_datamodoutline1" })
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_analyst_trends', p)
		writelog(e, 'yql_analyst_summary', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_analyst_trends', p)
		writelog(e, 'yql_analyst_summary', p)
		return 1
	except http.client.IncompleteRead as e:
		writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_analyst_trends', p)
		if (attempts < 3):
			r = yql_analyst_trends(tick, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_analyst_trends', p)	
			return 1

		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_analyst_trends', p)
			return 1



	i = 0
	cn = []
	count = True
	try:
		for ele in table:
			if (i == 3):
				for row in ele.findAll("tr"):
					if (i > 4):
						if count == True:
							ls = len(row)
							for t in range(0,ls - 1):
								cl = []
								cn.append(cl)
							count = False
						c = 0
						for col in row.findAll("td"):
							cs = col.get_text()
							cn[c].append(cs)
							c = c + 1
					i = i + 1
			i = i + 1
	except IndexError as e:
		p = []
		p.append(tick)
		writelog('[WARNING] INDEX ERROR Encountered', 'yql_analyst_trends', p)
		writelog(e, 'yql_analyst_trends', p)
		return 1
	for l in cn:
		s = 'INSERT INTO ' + tick + '_yql_analyst_trends (Strong_Buy, Buy, Hold, Underperform, Sell) VALUES ('
		for x in l:
			s = s + '\'' + x + '\', '
		s = s[:-2] + ')'
		dbquery(s)
	return 0
