__author__ = 'ssong'
from config import getconf
from logger import writelog
from yql_real import yql_real
import pymysql
import sys
import time

# Real time for evertything
def info_real_populate():
    p = []
    writelog('[INFO] Starting Info-Realtime Population','info_realtime',p)
    conn = pymysql.connect(host='localhost',port=3306, user='user', passwd='password', db='jsong')
    cur = conn.cursor()
    cur.execute("SELECT tick FROM ticklist")
    msg = '0'
    count = 1
    #for tick in cname:
    for tick1 in cur.fetchall():
        tick = tick1[0]
        print (str(count) + ": " + tick)
        count = count + 1 
        writelog('[INFO] realtime ' + tick, 'info_realtime', p)
        r = yql_real(tick, 0)
        time.sleep(1)
        if r == 1:
            p = []
            p.append(tick)
            writelog('[CRITICAL] Error Occurred During YQL_REALTIME', 'info_realtime', p)
        else:
            writelog('[SUCCESS] Successfully Retrieved Realtime data', 'info_realtime', p)
    cur.close()
    conn.close()
