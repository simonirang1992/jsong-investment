from pymysql import connect, err, sys, cursors, MySQLError 
from config import getconf
import sys
from decimal import *

def isDec(val):
        try:
                out = Decimal(val)
                return out
        except:
                return val

def dictreturn(query):
        dict={}
        try:
                cn = getconf('db')
                if not cn:
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
                                    val = isDec(value[i])
                                    #try:
                                    #        val = Decimal(value[i])
                                    #except:
                                    #        val = value[i]
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
        print (query)
        out=[]
        val = 0
        try:
                cn = getconf('db')
                if not cn:
                        sys.exit('Database Configuration Not Found --- Exiting...')
                conn = connect( host = cn[0], port = int(cn[1]), user= cn[2], passwd = cn[3], db = cn[4])
                cursor = conn.cursor()
                cursor.execute(query)
                for ele in cursor.fetchall():
                        val = isDec(ele)
                        #try:
                        #         val = Decimal(ele)
                        #except:
                        #         val = ele
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
                pass
        cursor.close()
        conn.close()
        return val
