from pymysql import connect, err, sys, cursors, MySQLError 
from logger import writelog
from config import getconf
import sys
from pymysql import connect, err, sys, cursors, MySQLError 
from config import getconf
import sys
from decimal import *

def dictreturn(query):
        getcontext().prec = 6
        dict={}
        try:
                cn = getconf('db')
                if not cn:
                        writelog('[CRITICAL] Unable to Read Database Configuration File!', 'selectdb', 'query')
                        sys.exit('Database Configuration Not Found --- Exiting...')
                conn = connect( host = cn[0], port = int(cn[1]), user= cn[2], passwd = cn[3], db = cn[4])
                cursor = conn.cursor()
                cursor.execute(query)
                desc = cursor.description
                nlist = len(desc)

                colname = []
                table = []
                for col in desc:
                          table.append([])
                dict = {}
                data = cursor.fetchall()         
                
                for value in data:
                           for i in range(0,nlist):
                                    try:
                                            val = Decimal(value[i])
                                    except:
                                            val = value[i]
                                    table[i].append(val)
                c = 0
                for col in desc:
                          dict[col[0]] = table[c]
                          c = c + 1              

        except MySQLError as e:
                p = []
                p.append(query)
                print (p)
                cursor.close()
                conn.close()
                sys.exit('MySQL Exception Found --- Exiting...')
        except Warning as e:
                p = []
                p.append(query)
                errmsg = '[CRITICAL] MYSQL Warning Detected' + str(e)
                pass
        cursor.close()
        conn.close()
        return dict
	




def selectdb(query):
        out=[]
        try:
                cn = getconf('db')
                if not cn:
                        writelog('[CRITICAL] Unable to Read Database Configuration File!', 'selectdb', 'query')
                        sys.exit('Database Configuration Not Found --- Exiting...')
                conn = connect( host = cn[0], port = int(cn[1]), user= cn[2], passwd = cn[3], db = cn[4])
                cursor = conn.cursor()
                cursor.execute(query)
                for ele in cursor.fetchall():
                        out.append(ele)
        except MySQLError as e:
                p = []
                p.append(query)
                print (p)
                errmsg = '[CRITICAL] MYSQL Error Detected' + str(e)
                writelog(errmsg, 'dbquery', p)
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
        return out
	
def dbquery(query):
	try:
		cn = getconf('db')
		if not cn:
			writelog('[CRITICAL] Unable to Read Database Configuration File!', 'dbquery', 'query')
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
		writelog(errmsg, 'dbquery', p)
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
		writelog('Unable to Read Database Configuration File!', 'dbquery', 'query')
		sys.exit('Database Configuration Not Found --- Exiting...')
	conn = connect( host = cn[0], port = int(cn[1]), user= cn[2], passwd = cn[3], db = cn[4])
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	cursor.close()
	conn.close()

#selectdb("SELECT tick FROM ticklist")
