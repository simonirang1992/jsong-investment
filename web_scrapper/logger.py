import os
import datetime
import time
from hipchat import err_hipchat
import sys

def writelog(msg, fname, param):
	msg = str(msg)
	inparam = 'Parameters: '
	if param:
		for ele in param:
			inparam = inparam + '\'' + str(ele) + '\', '
		inparam = inparam[:-2]

	c = 0
	path='log/'
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	logtype = 0
	msg = st + " Function Name: " + fname + ', ' + inparam + '\n' + msg + '\n'
	if ('[CRITICAL]' in msg) or ('[WARNING]' in msg):
		print (msg)
		#err_hipchat(msg)
		logtype = 1
	next = 1
	while True:
		name = 'jsong' + str(c) + '.log'
		try:
			if os.path.isfile(path + name):
				fs = os.path.getsize(path + name)
				if fs < 10000000:
					file = open(path + name, 'a')
					file.write(msg)
					file.close()
					break
				else:
					c = c + 1
			elif c == 0:
				file = open(path + name, 'a')
				file.write(msg)
				file.close()
				break
			else:
				file = open(path+name, 'a')
				file.write(msg)
				file.close()
				break
		except IOError as e:
			outerr = 'Fatal Error Encountered: %s' % e.strerror
			syslog.syslog(outerr)

	if (logtype == 1):
		try:
			c = 0
			while True:
				name = 'error' + str(c) + '.log'
				if os.path.isfile(path + name):
					fs = os.path.getsize(path + name)
					if fs < 10000000:
						file = open(path + name, 'a')
						file.write(msg)
						file.close()
						break
					else:
						c = c + 1
				elif c == 0:
					file = open(path + name, 'a')
					file.write(msg)
					file.close()
					break
				else:
					file = open(path+name, 'a')
					file.write(msg)
					file.close()
					break				
		except IOError as e:
                        outerr = 'Fatal Error Encountered: %s' % e.strerror
                        syslog.syslog(outerr)


