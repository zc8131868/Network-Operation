import telnetlib
import subprocess
import threading
import pexpect
import getpass
import sys

from IPy import IP
child = ""
show_result = ""
path = ""
class AutoNet(object):

	def __init__(self, username, pwd, device_ios):
		self.username = username
		self.pwd = pwd
		self.device_ios = device_ios
		# self.port = port
		# self.ip = ip
		# self.network = network

#check reachibility
	def _PING(self, ip, ping_able, ping_unable):
		try:
			subprocess.check_call('ping -c 1 %s' %ip, shell=True)
			ping_able.append(ip)
		except Exception as e:
			ping_unable.append(ip)

#check reachibility of given single ip address
	def PING_IP(self,ip):
		ping_able = []
		ping_unable = []
		ping_result = {"ping_able:":[], "ping_unable:":[]}
		self._PING(ip, ping_able, ping_unable)
		ping_result["ping_able:"] = ping_able
		ping_result["ping_unable:"] = ping_unable
		return(ping_result)

# check reachibility of ip addresses of given subnet
	def PING_Subnet(self, subnet):
		ping_able = []
		ping_unable = []
		ping_result = {"ping_able:":[], "ping_unable:":[]}
		threads = []
		subnet = IP(subnet)
		for ip in subnet:
			t = threading.Thread(target=self._PING, args=(str(ip),ping_able,ping_unable,))
			threads.append(t)

		for i in range(len(threads)):
			threads[i].start()

		for i in range(len(threads)):
			threads[i].join()
		#print("ping_able: %s" % ping_able)
		ping_result["ping_able:"] = ping_able
		ping_result["ping_unable:"] = ping_unable
		return(ping_result)

# login device with telnet or ssh automatically
	def auto_login(self, ip, username):
		name = username
		pwd = getpass.getpass("Pls input your password:")
		global child
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip
			child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			child.logfile_read = sys.stdout
			index = child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				child.sendline(name)
				child.expect("assword")
				try:
					child.sendline(pwd)
				except Exception as e:
					print(e)
			else:
				print("Cannot telnet this ip address %s" % ip)

		except:
			cmd_login_ssh = "ssh -l " + name + " " + ip
			child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			child.logfile_read = sys.stdout
			index = child.expect(["assword", pexpect.TIMEOUT])
			if index == 0:
				try:
					child.sendline(pwd)
				except Exception as e:
					print(e)

# show information on device
	def auto_show(self, cmd, URL=""):
		global path
		path = URL
		if path == "":
			child.expect("#")
			child.sendline("ter len 0")
			child.expect("#")
			child.sendline(cmd)
		else:
			global show_result
			show_result = open(path, "w")
			child.expect("#")
			child.sendline("ter len 0")
			child.expect("#")
			child.sendline(cmd)
			child.logfile = show_result
			#child.expect(pexpect.EOF)

# Terminate the conncetion
	def close_connection(self):
		if path == "":
			child.expect("#")
			child.sendline("exit")
			child.close()
		else:
			child.expect("#")
			child.sendline("exit")			
			child.close()
			show_result.close()








		


