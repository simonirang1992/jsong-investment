import sys
from decimal import Decimal
from db_formula import selectdb, dictreturn

def isint(val):
	try:
		int(val)
		return True
	except:
		return False

def jql (*args):
	nargs = len(args)
	if (args[0] == "sum") & ((nargs >= 3) & (nargs <= 5)):
		query = "SELECT SUM(" + args[2] + ") FROM " + args[1]
		if (nargs == 5):
			if (isint(args[3])) & (isint(args[3])):
				query = query + " WHERE id >= " + str(args[3]) + " AND id <= " + str(args[4])
		elif (nargs == 4):
			if (not isint(args[3])):
				query = query + " WHERE " + str(args[3])
		out = selectdb(query)
	elif (args[0] =="get") & ((nargs >= 3) & (nargs <= 5 )):
		query = "SELECT " + args[2] + " FROM " + args[1]
		if (nargs == 4):
			if (isint(args[3])):
				query = query + " WHERE id = " + str(args[3]) + ";"
			else:
				query = query + " WHERE " + args[3]
		elif (nargs == 5):
			if (isint(args[3])) & (isint(args[4])):
				query = query + " WHERE id >= " + str(args[3]) + " AND id <= " + str(args[4])
		query = query + " limit 1"
		out = selectdb(query)
	elif (args[0] =="gets") & (nargs >= 3) & (nargs<=5):
		query = "SELECT "
		for col in args[2]:
			query = query + col + ", "
		query = query[:-2] + " FROM " + args[1]
		if (nargs == 4):
			if (isint(args[3])):
				query = query + " WHERE id = " + str(args[3])
			else:
				query = query + " WHERE " + args[3]
		elif (nargs == 5):
			query = query + " WHERE id >= " + str(args[3]) + " AND id <= " + str(args[4])
		query = query + ";"
		out = dictreturn(query)
	elif (args[0] =="maxcol") & (nargs == 2):
		query = "SELECT COUNT(*) FROM " + args[1] + ";"
		out = selectdb(query)
	else:
		print ("Unknown Command")
		sys.exit()
	print (out)	
