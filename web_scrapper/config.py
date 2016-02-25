from logger import writelog

def getconf(category):
	try:
		conf = open('config/' + category + '.cfg', 'r')
		li = []
		for var in conf:
			var = var[:-1]
			var = var.replace(" ","")
			li.append(var)
		return li
	except IOError as e:
		errmsg = '[CRITICAL] Error occured at config.py: %s' % e.strerror
		p = []
		p.append(category)
		writelog(errmsg, "getconf", p)
		g = []
		return g 
