from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from db import selectdb
from config import getconf
import sys
import http.client
import time
from decimal import *
def updatetick():
	out = selectdb("SELECT id, tick, sector, industry FROM ticklist where id < 5")
	print (out['tick'][0])	
#	for tick in out:
#		print ("")


		
updatetick()
