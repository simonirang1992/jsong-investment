from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
import sys
from logger import writelog
import datetime
import http.client
def yql_hist_init(tick):
	dquery = 'DROP TABLE IF EXISTS ' + tick + '_hist'
	dberase(dquery)

	#create table
	cquery = 'CREATE TABLE ' + tick + '_hist (id INT NOT NULL AUTO_INCREMENT, volume VARCHAR(20), adjclose VARCHAR(10), PRIMARY  KEY (id))'
	dbquery(cquery)
	return 0

def yql_hist(tick, years, attempts):
	p = []
	p.append(tick)
	p.append(years)
	p.append(attempts)
	now = datetime.datetime.now()
	yeara = now.year
	montha = now.month
	daya = now.day

	yearb = now.year - 10
	monthb = now.month - 1
	dayb = now.day - 2
	if monthb == 0:
		monthb = 1

	if dayb <= 0:
		dayb = 1
	
	# Web Scrapping
	try:
		req = Request(
			'https://ca.finance.yahoo.com/q/hp?s=' + tick + '&a=' + str(monthb) + '&b=' + str(dayb) + '&c='+ str(yearb) + '&d=' + str(montha) + '&e=' + str(daya) + '&f=' + str(yeara) + '&g=w',
			data=None,
			headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
		html = urlopen(req)
		data = html.read()

		#  Find table & parase
		soup = BeautifulSoup(data, 'html.parser')
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_hist', p)
		writelog(e, 'yql_hist', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_hist', p)
		writelog(e, 'yql_hist', p)
		return 1
	except http.client.IncompleteRead as e:
                writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_hist', p)
                if (attempts < 3):
                        r = yql_growth(tick, attempts + 1)
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_hist', p)
                        return 1

                if (r == 0):
                        return 0
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_hist', p)
                        return 1

	# Remove subscripts
	for tag in soup.find_all('sup'):
		tag.replaceWith('')

	table = soup.find("table", { "class" : "yfnc_datamodoutline1" })

	first = True
	# init
	try:
		ttable = table.findAll("table")
		for t in ttable:
			for row in t.findAll("tr"): #table.findAll("tr"):
				
				iquery = 'INSERT INTO ' + tick + '_hist (volume, adjclose) VALUES ('
				if len(row) == 7 and first == False:
					s = 0
					for col in row.findAll("td"):
						if (s == 1):
							last = col.get_text()
						if (s == 5) | (s == 6):
							tv = col.get_text()
							tv = tv.replace(',','')
							iquery = iquery + tv + ', '
						s = s + 1
					iquery = iquery[:-2] + ')'
					#print (iquery)
					dbquery(iquery)
				else:
					first = False

		for i in range(1,years):
			g = yql_hist_rep(tick, i ,last, 0)
			if g == 1:
				break
	except IndexError as e:
		writelog('[WARNING] INDEX ERROR Encountered', 'yql_hist', p)
		writelog(e, 'yql_hist', p)
		return 1
	return 0

def yql_hist_rep(tick, yc, last, attempts):
	p = []
	p.append(tick)
	p.append(yc)
	p.append(last)
	p.append(attempts)
	now = datetime.datetime.now()
	yeara = now.year
	montha = now.month
	daya = now.day
	yearb = now.year - 10
	monthb = now.month - 1
	dayb = now.day - 2
	if monthb == 0:
	        monthb = 1
	if dayb <= 0:
	        dayb = 1
	
	yc = yc * 66
	try:
		req = Request(
			'https://ca.finance.yahoo.com/q/hp?s=' + tick +'&a=' + str(monthb) + '&b=' + str(dayb) + '&c='+ str(yearb) + '&d=' + str(montha) + '&e=' + str(daya) + '&f=' + str(yeara) + '&g=w&z=66&y=' + str(yc),
			data=None,
			headers={
					 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)

		html = urlopen(req)
		data = html.read()

		soup = BeautifulSoup(data, 'html.parser')
	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'yql_hist_rep', p)
		writelog(e, 'yql_hist_rep', p)
		return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'yql_hist_rep', p)
		writelog(e, 'yql_hist_rep', p)
		return 1
	except http.client.IncompleteRead as e:
                writelog('[WARNING] HTTP INCOMPLETE ERROR', 'yql_hist_rep', p)
                if (attempts < 3):
                        r = yql_hist_rep(tick, yc, last, attempts + 1)
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'yql_hist_rep', p)
                        return 1

                if (r == 0):
                        return 0
                else:
                        writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'yql_hist_rep', p)
                        return 1
	# Remove subscripts
	for tag in soup.find_all('sup'):
		tag.replaceWith('')

	table = soup.find("table", { "class" : "yfnc_datamodoutline1" })
	ttable = table.findAll("table")
	first = True
	try:
		for t in ttable:
			for row in t.findAll("tr"): #table.findAll("tr"):
				iquery = 'INSERT INTO ' + tick + '_hist (volume, adjclose) VALUES ('
				if len(row) == 7 and first == False:
					s = 0
					for col in row.findAll("td"):
						if (s == 1):
							clast = col.get_text()
							if last == clast:
								return 1
						if (s == 5) | (s == 6):
							tv = col.get_text()
							tv = tv.replace(',','')
							iquery = iquery + tv + ', '
						s = s + 1
					iquery = iquery[:-2] + ')'
					dbquery(iquery)
				else:
					first = False
	except IndexError as e:
		writelog('[WARNING] INDEX ERROR Encountered', 'yql_hist_rep', p)
		writelog(e, 'yql_hist_rep', p)
		return 1
	return (clast)
