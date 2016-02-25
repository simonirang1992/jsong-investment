from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from db import dbquery, dberase
from config import getconf
from logger import writelog
import sys
from http.client import HTTPConnection

def amigo_init(tick, category, freq):
	# Get column name
	cname = getconf(category)
	if not cname:
		p = []
		p.append(tick)
		p.append(category)
		p.append(freq)
		writelog('[CRITICAL] No Configuration File Found', 'amigo_init', p)
		sys.exit('[CRITICAL] No Configuration File Found')
		return 1
	tname = 'amigo_' + tick + '_' + category.replace('-','_') + '_' + freq

    	# Erase WipeOut Old table
	tdrop = 'DROP TABLE IF EXISTS ' + tname
	dberase(tdrop)

	# Create table
	tcreate1 = 'CREATE TABLE ' +  tname + ' ( id INT(3) UNSIGNED AUTO_INCREMENT PRIMARY KEY, '
	tcreate2 = ''
	for li in cname:
		tcreate2 = tcreate2 + str(li) + ' VARCHAR(10), '
	tcreate2 = tcreate2[:-2] + ')'
	dbquery(tcreate1 + tcreate2)
	return 0

def amigo(tick, category, freq, attempts):
	p = []
	p.append(tick)
	p.append(category)
	p.append(freq)
	p.append(attempts)

	try:
		# Web Scrapping
		req = Request(
			'http://amigobulls.com/stocks/' +  tick + '/' + category + '/' + freq,
			data=None,
			headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
		html = urlopen(req)

		soup = BeautifulSoup(html, 'html.parser')
		for tag in soup.find_all('sup'):
			tag.replaceWith('')
		table = soup.find("table", { "id" : "stackinfo" })

	except URLError as e:
		writelog('[CRITICAL] URL ERROR Encountered', 'amigo', p)
		if (attempts < 3):
			r = amigo(tick, category, freq, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'amigo', p)
			return 1
		
		print ("Attempt Number: " + str(attempts) + " Result: " + str(r))
		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'amigo', p)
			writelog(e, 'amigo', p)
			return 1
	except HTTPError as e:
		writelog('[WARNING] HTTP ERROR Encountered', 'amigo', p)
		writelog(e, 'amigo', p)
		return 1
	except http.client.IncompleteRead as e:
		writelog('[WARNING] HTTP INCOMPLETE ERROR', 'amigo', p)
		if (attempts < 3):
			r = amigo(tick, category, freq, attempts + 1)
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE ERROR AFTER 3 TRIES', 'amigo', p)	
			return 1
		print ("Attempt Number: " + str(attempts) + " Result: " + str(r))
		if (r == 0):
			return 0
		else:
			writelog('[CRITICAL] HTTP INCOMPLETE READ ERROR - Unable to resolve', 'amigo', p)
			return 1

	# init
	init = False
	cl = []
	cd = []

	for r in table.findAll("tr"):
		for e in r.findAll("td"):
			cd.append([])
		break

	for row in table.findAll("tr"):
		if (init == True): 	
			s = True
			c = 0
			for col in row.findAll("td"):
				ltd = col.get_text()
				ltd = ltd.replace("-","")
				ltd = ltd.replace(" ","")
				if (s == True):
					cl.append(ltd)
					s = False
				else:
					cd[c].append(ltd)
					c = c + 1
		else:
			init = True

	cname = getconf(category)
	if not cname:
		p = []
		p.append(tick)
		p.append(category)
		p.append(freq)
		writelog('[CRITICAL] No Configuration File Found', 'amigo', p)
		sys.exit('[CRITICAL] No Configuration File Found')
	base = 'INSERT INTO ' + 'amigo_' + tick + '_' + category.replace('-','_') + '_' + freq + ' ('

	for li in cname:
		base = base + li + ', '
	base = base[:-2] + ') VALUES ('

	lcd = len(cd) - 1
	cd.pop(lcd)
	retval = 0
	for z in cd:
		tinsert = base
		if z:
			if (len(cname) ==len(z)):
				for cz in z:
					tinsert = tinsert + '\'' + cz + '\'' + ', '
				tinsert = tinsert[:-2] + ');'
				dbquery(tinsert)
			else:
				retval = 1
	return retval



