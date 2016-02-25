from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
from logger import writelog
import http.client

# Initialize
def yql_estimates_init(tick):
	cn = getconf('estimates')
	if not cn:
		p = []
		p.append(tick)
		writelog('[CRITICAL] No Configuration File Found', 'yql_estimates_init', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	d = 'DROP TABLE IF EXISTS ' + tick + '_yql_estimates'
	dberase(d)

	s = 'CREATE TABLE ' + tick + '_yql_estimates (id INT NOT NULL AUTO_INCREMENT, '
	for ele in cn:
		s = s + ele + ' VARCHAR(15), '
	s = s[:-2] + ', PRIMARY KEY(id))'
	dbquery(s)
	return 0

# Collects Beta
def yql_estimates(tick, attempts):
	p = []
	p.append(tick)
	p.append(attempts)
    # Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/q/ae?s=' + tick + '+Analyst+Estimates',
			data=None,
			headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
			}
		)
		html = urlopen(req)
		data = html.read()
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered ' + str(e), 'yql_estimates', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered ' + str(e), 'yql_estimates', p)
		return 1
	except http.client.IncompleteRead as e:
                writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_estimates', p)
                if (attempts < 3):
                        r = yql_competitor(tick, attempts + 1)
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_estimates', p)
                        return 1

                if (r == 0):
                        return 0
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_estimates', p)
                        return 1
    # Find table & Parse
	soup = BeautifulSoup(data, 'html.parser')

	# Remove subscripts
	for tag in soup.find_all('sup'):
		tag.replaceWith('')

	table = soup.find_all("table", { "class" : "yfnc_tableout1" })

	cn = getconf('estimates')

	s = 'INSERT INTO ' + tick + '_yql_estimates ('
	try:
		for ele in cn:
			s = s + ele + ', '
		s = s[:-2] + ') VALUES ('

		c = 0
		ccn = [[],[],[],[]]
		for ele in table:
			if (c >= 0) and (c <= 2):
				for row in ele.findAll("tr"):
					for tag in row.find_all(['table','style']):
								tag.replaceWith('')
					i = 0
					for col in row.findAll("td"):
						if (i > 0):
							ccn[i - 1].append(col.get_text())
						i = i + 1
			c = c + 1
	except IndexError as e:
		p = []
		p.append(tick)
		writelog('[WARNING] INDEX ERROR Encountered', 'yql_estimates', p)
		writelog(e, 'yql_estimates', p)
		return 1
	retval = 0
	for cr in ccn:
		ss = s
		if (len(cr) == len(cn)):
			for cc in cr:
				ss = ss + '\'' + cc + '\', '
			ss = ss[:-2] + ')'
			dbquery(ss)
		else:
			retval = 1
	return retval
