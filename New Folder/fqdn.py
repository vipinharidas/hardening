import re

def check_fqdn(fdn):
	t = re.search(r'([a-zA-Z0-9]*\.[a-zA-Z0-9]*\.[a-zA-Z0-9]*$)',fdn)
	if t:
		return fdn
	else:
		return (fdn+" needs work")

while (1 > 0):
	i = input ('?')
	print (check_fqdn(i))

