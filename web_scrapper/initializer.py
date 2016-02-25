__author__ = 'ssong'
from amigo import amigo_init
from yql_analystsummary import yql_analyst_summary_init
from yql_analysttrends import yql_analyst_trends_init
from yql_competitors import yql_competitor_init
from yql_day import yql_day_init
from yql_dividends import yql_dividends_init
from yql_estimates import yql_estimates_init
from yql_growth import yql_growth_init
from yql_highlight import yql_highlight_init
from yql_hist import yql_hist_init
from yql_real import yql_real_init
from config import getconf
from logger import writelog
import sys

def init_db():
	p = []
	writelog('[INFO] Starting Database Initializer', 'initializer',p)

	cname = getconf("ticklist")
	if not cname:
		writelog('[CRITICAL] No Configuration File Found', 'initializer', p)
		sys.exit('[CRITICAL] No Configuration File Found')

	# Single Table
	if (yql_analyst_summary_init() == 0):
		writelog('[SUCCESS] Initialized yql_analyst_summary table', 'initializer', p)
	else:
		writelog('[CRITICAL] Unable to create database yql_analyst_summary', 'initializer', p)
		sys.exit('[CRITICAL] Unable to create database yql_analyst_summary')

	if (yql_day_init() == 0):
		writelog('[SUCCESS] Initialized yql_day table', 'initializer', p)
	else:
		writelog('[CRITICAL] Unable to create database yql_day table', 'initializer', p)
		sys.exit('[CRITICAL] Unable to create database yql_day table')

	if (yql_dividends_init() == 0):
		writelog('[SUCCESS] Initialized yql_day table', 'initializer', p)
	else:
		writelog('[CRITICAL] Unable to create database yql_day table', 'initializer', p)
		sys.exit('[CRITICAL] Unable to create database yql_day table')

	if (yql_highlight_init() == 0):
		writelog('[SUCCESS] Initialized yql_highlight table', 'initializer', p)
	else:
		writelog('[CRITICAL] Unable to create database yql_highlight table', 'initializer', p)
		sys.exit('[CRITICAL] Unable to create database yql_highlight table')

	if (yql_real_init() == 0):
		writelog('[SUCCESS] Initialized yql_real table', 'initializer', p)
	else:
		writelog('[CRITICAL] Unable to create database yql_real table', 'initializer', p)
		sys.exit('[CRITICAL] Unable to create database yql_real table')

	term = "quarterly"
	for tick in cname:
		tick = tick.replace(" ","")
		if (amigo_init(tick, "balance-sheet", term) == 0):
			tname = 'amigo_' + tick + '_' + "balance_sheet" + '_' + term
			writelog('[SUCCESS] Initialized ' + tname + ' table', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tname + ' table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tname + ' table')

		if (amigo_init(tick, "cash-flow", term) == 0):
			tname = 'amigo_' + tick + '_' + "cash_flow" + '_' + term
			writelog('[SUCCESS] Initialized ' + tname + ' table', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tname + ' table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tname + ' table')

		if (amigo_init(tick, "income-statement", term) == 0):
			tname = 'amigo_' + tick + '_' + "income_statement" + '_' + term
			writelog('[SUCCESS] Initialized ' + tname + ' table', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tname + ' table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tname + ' table')

		if (yql_analyst_trends_init(tick) == 0):
			writelog('[SUCCESS] Initialized ' + tick + '_yql_analyst_trends', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tick + '_yql_analyst_trends table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_analyst_trends table')

		if (yql_competitor_init(tick) == 0):
			writelog('[SUCCESS] Initialized ' + tick + '_yql_competitor', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tick + '_yql_competitor table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_competitor table')

		if (yql_estimates_init(tick) == 0):
			writelog('[SUCCESS] Initialized ' + tick + '_yql_estimates', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tick + '_yql_estimates table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_estimates table')

		if (yql_growth_init(tick) == 0):
			writelog('[SUCCESS] Initialized ' + tick + '_yql_growth', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tick + '_yql_growth table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_growth table')

		if (yql_hist_init(tick) == 0):
			writelog('[SUCCESS] Initialized ' + tick + '_yql_hist', 'initializer', p)
		else:
			writelog('[CRITICAL] Unable to create database ' + tick + '_yql_hist table', 'initializer', p)
			sys.exit('[CRITICAL] Unable to create database ' + tick + '_yql_hist table')

	writelog('[SUCCESS] Initializing Database Tables Complete!', 'initializer', p)


init_db()
