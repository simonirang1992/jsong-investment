import glob
totalsum = 0
for filename in glob.glob('*.php'):
	with open(filename) as f:
		ftotal = sum(1 for _ in f)
		##print (ftotal)
	totalsum = totalsum + ftotal
	
print (totalsum)
