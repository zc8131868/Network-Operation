import re
############################################################################
def cisco_nxos_sn(file):
	res = re.search("Serial Number.+", file.read())
	result = re.findall("Serial Number.+: (.+)", res.group())
	return(result)

def cisco_ios_sn(file):
	res = re.findall("System serial number.+: (.+)", file.read())
	return(res)

def rg_os_sn(file):
	res = re.findall("Serial number.+ : (.+)", file.read())
	return(res)
############################################################################
def cisco_nxos_sv(file):
	res = re.findall("(?:system:.+version |NXOS: version )(.+)", file.read())
	return(res)

def cisco_ios_sv(file):
	res = re.search("Version (.+)", file.read())
	result = re.findall("Version (.+),", res.group())
	return(result)

def rg_os_sv(file):
	res = re.findall("System software version : RGOS (.+) ", file.read())
	return(res)
############################################################################
