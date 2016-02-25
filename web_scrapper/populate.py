__author__ = 'ssong'
from amigo import amigo_init, amigo
from yql_analystsummary import yql_analyst_summary_init, yql_analyst_summary
from yql_analysttrends import yql_analyst_trends_init, yql_analyst_trends
from yql_competitors import yql_competitor_init, yql_competitor
from yql_day import yql_day_init, yql_day
from yql_dividends import yql_dividends_init, yql_dividends
from yql_estimates import yql_estimates_init, yql_estimates
from yql_growth import yql_growth_init, yql_growth
from yql_highlight import yql_highlight_init, yql_highlight
from yql_hist import yql_hist_init, yql_hist
from config import getconf
from logger import writelog
from db import dbquery, dberase
import sys
import time

def functostr(cl):
	s = ''
	for ele in cl:
		s = s + ele + ','
	s = s[:-1]
	return s

def populate(list, deletet, start):
	p = []
	p.append(list)
	p.append(deletet)
	writelog('[INFO] Populating Ticklist Number :', 'populate', p)
	cname = getconf("ticklist_p" + str(list))
	if not cname:
		writelog('[CRITICAL] No Configuration File Found', 'populate', p)
		sys.exit('[CRITICAL] No Configuration File Found')

	term = "quarterly"
	ctick = ''
	rcl = []
	total = len(cname)
	counter = 0

	if (deletet == 1):
		writelog('[INFO] Dropping and Creating New Table', 'populate', p)
		s = "DROP TABLE IF EXISTS ticklist"
		dberase(s)
		s = "CREATE TABLE ticklist (id INT NOT NULL AUTO_INCREMENT, tick VARCHAR(10) NOT NULL, enabled VARCHAR(5) NOT NULL, status VARCHAR(5) NOT NULL, manual VARCHAR(5) NOT NULL, marketcap VARCHAR(20), sector VARCHAR(100), industry VARCHAR(100), errorfnc VARCHAR(200), enabledp VARCHAR(100), PRIMARY KEY(id))"
		dbquery(s)
	for tick in cname:
		counter = counter + 1
		if (counter >= start):
			outputstr = (str(counter)) + ":" + tick
			print (outputstr)
			writelog('[INFO] Progress: ' + str(counter) + ' / ' + str(total), 'populate', p)
			success = 0
			failure = 0
			failed_functions = []

			writelog('[INFO] Re-Initializing Tables Now......(' + tick + ')', 'populate', p)
			if (amigo_init(tick, "balance-sheet", term) == 0):
				tname = 'amigo_' + tick + '_' + "balance_sheet" + '_' + term
				writelog('[SUCCESS] Initialized ' + tname + ' table', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tname + ' table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tname + ' table')
			time.sleep(1)
			if (amigo_init(tick, "cash-flow", term) == 0):
				tname = 'amigo_' + tick + '_' + "cash_flow" + '_' + term
				writelog('[SUCCESS] Initialized ' + tname + ' table', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tname + ' table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tname + ' table')
			time.sleep(1)
			if (amigo_init(tick, "income-statement", term) == 0):
				tname = 'amigo_' + tick + '_' + "income_statement" + '_' + term
				writelog('[SUCCESS] Initialized ' + tname + ' table', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tname + ' table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tname + ' table')

			if (yql_analyst_trends_init(tick) == 0):
				writelog('[SUCCESS] Initialized ' + tick + '_yql_analyst_trends', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tick + '_yql_analyst_trends table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_analyst_trends table')

			if (yql_competitor_init(tick) == 0):
				writelog('[SUCCESS] Initialized ' + tick + '_yql_competitor', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tick + '_yql_competitor table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_competitor table')
	
			if (yql_estimates_init(tick) == 0):
				writelog('[SUCCESS] Initialized ' + tick + '_yql_estimates', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tick + '_yql_estimates table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_estimates table')

			if (yql_growth_init(tick) == 0):
				writelog('[SUCCESS] Initialized ' + tick + '_yql_growth', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tick + '_yql_growth table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_growth table')
	
			if (yql_hist_init(tick) == 0):
				writelog('[SUCCESS] Initialized ' + tick + '_yql_hist', 'populate', p)
			else:
				writelog('[CRITICAL] Unable to create database ' + tick + '_yql_hist table', 'populate', p)
				sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_hist table')

			writelog('[INFO] Populating Tables Now......(' + tick + ')', 'populate', p)

			if (amigo(tick, "balance-sheet", term, 0) == 0):
				success = success + 1
			else:
				failure = failure + 1
				ff = "amigo-balance-sheet"
				failed_functions.append(ff)

			if (amigo(tick, "cash-flow", term, 0) == 0):
				success = success + 1
			else:
				failure = failure + 1
				ff = "amigo-cash-flow"
				failed_functions.append(ff)

			if (amigo(tick, "income-statement", term, 0) == 0):
				success = success + 1
			else:
				failure = failure + 1
				ff = "amigo-income-statement"
				failed_functions.append(ff)

			if (yql_analyst_summary(tick, 0) == 0):
				success = success + 1
			else:
				failure = failure + 1
				ff = "yql_analyst_summary"
				failed_functions.append(ff)

			if (yql_analyst_trends(tick, 0) == 0):
				success = success + 1
			else:
				failure = failure + 1
				ff = "yql_analyst_trends"
				failed_functions.append(ff)

			if (yql_competitor(tick, 0) == 0):
				success = success + 1
			else:
				failure = failure + 1
				ff = "yql_competitor"
				failed_functions.append(ff)
	
			if (yql_day(tick, 0) == 0):
				success = success + 1
			else:
				ff = "yql_day"
				failed_functions.append(ff)

			if (yql_dividends(tick, 0) == 0):
				success = success + 1
			else:
				ff = "yql_dividends"
				failed_functions.append(ff)
	
			if (yql_estimates(tick, 0) == 0):
				success = success + 1
			else:
				ff = "yql_estimates"
				failed_functions.append(ff)

			if (yql_growth(tick, 0) == 0):
				success = success + 1
			else:
				ff = "yql_growth"
				failed_functions.append(ff)

			if (yql_highlight(tick, 0) == 0):
				success = success + 1
			else:
				ff = "yql_highlight"
				failed_functions.append(ff)

			writelog('[INFO] Populating Database Tables Complete! ' + '(' + tick + ')', 'populate', p)
		
			# Delete Row
			dquery = 'DELETE FROM ticklist WHERE tick = \'' + tick + '\''
			dbquery(dquery)


			if (failure > 0):
				flist = functostr(failed_functions)
				wmsg = '[WARNING] Encountered Some Failures While Populating Database for ' + tick + '. \nSuccess: ' + str(success) + '  Failure: ' + str(failure) + '\nList of Failed Functions: ' + flist
				writelog(wmsg, 'populate', p)
				s = "INSERT INTO ticklist (tick, enabled, status, manual, errorfnc) VALUES (\'" + tick + "\', \'1\', \'1\', \'1\', \'" + flist + "\')"
			else:
				writelog('[SUCCESS] Populated Database Tables For ' + tick + ' Without Error', 'populate', p)
				s = "INSERT INTO ticklist (tick, enabled, status, manual) VALUES (\'" + tick + "\', \'1\', \'0\', \'1\')"				
			dbquery(s)
			time.sleep(7)
	writelog('[INFO] Finished Populating Database', 'populate', p)
	writelog('[INFO] Finished Populating Ticklist Number: ' + str(list), 'populate', p)
