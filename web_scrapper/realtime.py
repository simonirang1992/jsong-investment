__author__ = 'ssong'
from config import getconf
from logger import writelog
from yql_real import yql_real
import pymysql
import sys
import time

# REAL TIME FOR SELECTED COMPANIES
def real_populate():
    p = []
    writelog('[INFO] Starting Realtime Population','real_populate',p)
    conn = pymysql.connect(host='localhost',port=3306, user='user', passwd='password', db='jsong')
    cur = conn.cursor()
    cur.execute("SELECT tick FROM ticklist WHERE enabled = 1")

    msg = '0'
    count = 1
    #for tick in cname:
    for tick1 in cur.fetchall():
        tick = tick1[0]
        print (str(count) + ": " + tick)
        count = count + 1 
        writelog('[INFO] realtime ' + tick, 'real_populate', p)
        r = yql_real(tick, 0)
        if r == 1:
            p = []
            p.append(tick)
            writelog('[CRITICAL] Error Occurred During YQL_REALTIME', 'real_populate', p)
        else:
            writelog('[SUCCESS] Successfully Retrieved Realtime data', 'real_populate', p)
    cur.close()
    conn.close()
