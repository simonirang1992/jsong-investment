from pymysql import connect, err, sys, cursors, MySQLError 
from config import getconf
import sys
from pymysql import connect, err, sys, cursors, MySQLError 
from config import getconf
import sys

	
def dbquery(query):
	try:
		cn = getconf('db')
		if not cn:
			sys.exit('Database Configuration Not Found --- Exiting...')
		conn = connect( host = cn[0], port = int(cn[1]), user= cn[2], passwd = cn[3], db = cn[4])
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
	except MySQLError as e:
		p = []
		p.append(query)
		print (p)
		errmsg = '[CRITICAL] MYSQL Error Detected' + str(e)
		cursor.close()
		conn.close()
		sys.exit('MySQL Exception Found --- Exiting...')
	except Warning as e:
		p = []
		p.append(query)
		errmsg = '[CRITICAL] MYSQL Warning Detected' + str(e)
		writelog(errmsg, 'dbquery', p)
		pass
	cursor.close()
	conn.close()

def dberase(query):
	cn = getconf('db')
	if not cn:
		sys.exit('Database Configuration Not Found --- Exiting...')
	conn = connect( host = cn[0], port = int(cn[1]), user= cn[2], passwd = cn[3], db = cn[4])
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	cursor.close()
	conn.close()

#selectdb("SELECT tick FROM ticklist")
