import telnetlib
import subprocess
import threading
import pexpect
import getpass
import sys
import re
import time
import methodlib 
from IPy import IP


def zgc(ip_set):
	username = "chengzheng"
	passwd = "zhengc###"
	for ip in ip_set:
		with open(" ", "w+") as result_file:
			cmd_login_telnet = "telnet " + ip
			child = pexpect.spawn(cmd_login_telnet, timeout=5, encoding='utf-8')
			child.logfile_read = result_file
			child.logfile = sys.stdout
			index = child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				child.sendline(username)
				child.expect('assword')
				child.sendline(passwd)
				child.expect("#")
				child.sendline("show ip int b")
				child.expect("#")
				result_file.seek(0)
				show_ip_int = result_file.readlines()
				# indicater = result_file.tell()
				for line in show_ip_int:
					res = re.findall("VLAN \d+", line)
					if res:
						# result_file.seek(indicater)
						indicater = result_file.tell()
						child.sendline("show run int " + res[0])
						child.expect("#")
						result_file.seek(indicater)
						show_run_int = result_file.readlines()
						show_run_int = " ".join(show_run_int)
						dhcp = re.findall("ip helper-address", show_run_int)
						if dhcp :
							child.sendline("config")
							child.expect("#")
							child.sendline("int "+res[0])
							child.expect("#")
							child.sendline("no ip helper-address 30.31.255.133")
							child.expect("#")
							child.sendline("ip helper-address 30.26.192.21")
							child.expect("#")
							child.sendline("end")
							child.expect("#")
							child.sendline("wr")
							child.expect("#")
				child.sendline("exit")
			else:
				print("Cannot telnet this ip address %s" % ip)



