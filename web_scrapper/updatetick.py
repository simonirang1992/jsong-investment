from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase,selectdb
from config import getconf
import sys
from logger import writelog
import http.client
import time

def updatetick():
	out = selectdb("SELECT tick FROM ticklist")	
	for tick in out:
		tick1=tick[0]
		print (tick1)
		yql_updatetick(tick1,0)
		time.sleep(1)
# Collects Beta
def yql_updatetick(tick,attempts):
	p = []
	p.append(tick)
	p.append(attempts)
	# Web Scrapping
	try:
		req = Request(
			'http://finance.yahoo.com/q/in?s=' + tick,
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
		writelog('[CRITICAL] URL ERROR Encountered', 'updatetick', p)
		writelog(e, 'updatetick', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'updatetick', p)
		writelog(e, 'updatetick', p)
		return 1
	except http.client.IncompleteRead as e:
		writelog('[WARNING] HTTP INCOMPLETE ERROR', 'updatetick', p)
		if (attempts < 3):
			r = yql_updatetick(tick, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'updatetick', p)	
			return 1

		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'updatetick', p)
			return 1

	i = 0
	cn = []
	count = True
	try:
		for ele in table:
			for tr in ele.findAll("tr"):
				if i >= 1:
					for td in tr.findAll("td"):
						cn.append(td.get_text())
				i = i + 1
	except IndexError as e:
		p = []
		p.append(tick)
		writelog('[WARNING] INDEX ERROR Encountered', 'updatetick', p)
		writelog(e, 'updatetick', p)
		return 1
	if (len(cn) == 2):
		s = "UPDATE ticklist SET sector = \'" + cn[0] + "\', industry = \'" + cn[1] + "\' WHERE tick = \'" + tick + "\'"
		dbquery(s)
	return 0
updatetick()
