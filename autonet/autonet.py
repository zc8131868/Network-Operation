import telnetlib
import subprocess
import threading
import pexpect
import getpass
import sys
import re
import time

from IPy import IP
child = ""
show_result = ""
path = ""
class AutoNet(object):

	def __init__(self, username, device_ios):
		self.username = username
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

# show command via telnet or ssh
	def auto_show(self, ip, cmd, URL=" "):
		name = self.username
		pwd = getpass.getpass("Pls input your password:")
		global child
		global show_result
		show_result = open(URL, "w")
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip	
			child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			child.logfile = show_result
			child.logfile_read = sys.stdout
			index = child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				child.sendline(name)
				child.expect("assword")
				try:
					child.sendline(pwd)
					child.expect("#")
					child.sendline("ter len 0")
					child.expect("#")
					child.sendline(cmd)
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + name + " " + ip
			child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			child.logfile = show_result
			child.logfile_read = sys.stdout
			index = child.expect(["assword", pexpect.TIMEOUT])
			if index == 0:
				try:
					child.sendline(pwd)
					child.expect("#")
					child.sendline("ter len 0")
					child.expect("#")
					child.sendline("#")
				except Exception as e:
					print(e)
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			error_file = open("error_ip", "w")
			error_file.write(ip)
			error_file.write("#########################")


# download configuration with single cmd
	def auto_config(self, ip, cmd, URL=" "):
		name = self.username
		pwd = getpass.getpass("Pls input your password:")
		global child
		global show_result
		show_result = open(URL, "w")
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip
			child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			child.logfile = show_result
			child.logfile_read = sys.stdout
			index = child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				child.sendline(name)
				child.expect("assword")
				try:
					child.sendline(pwd)
					child.expect("#")
					child.sendline("config")
					child.sendline("\n")
					child.expect("#")
					child.sendline(cmd)
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + name + " " + ip
			child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			child.logfile = show_result
			child.logfile_read = sys.stdout
			index = child.expect(["assword", pexpect.TIMEOUT])
			if index == 0:
				try:
					child.sendline(pwd)
					child.expect("#")
					child.sendline("config")
					child.sendline("\n")
					child.expect("#")
					child.sendline(cmd)
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			error_file = open("error_ip", "w")
			error_file.write(ip)
			error_file.write("#########################")


# download configuration from file
	def auto_config_file(self, ip, file, URL=" "):
		name = self.username
		global child
		global show_result
		cmd_list =[]
		pwd = getpass.getpass("Pls input your password:")
		cmd_file = open(file)
		show_result = open(URL, "w")
		for i in cmd_file:
			cmd_list.append(re.sub("\n", "", i))
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip
			child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			child.logfile = show_result
			child.logfile_read = sys.stdout
			index = child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				child.sendline(name)
				child.expect("assword")
				try:
					child.sendline(pwd)
					child.expect("#")
					child.sendline("config")
					child.sendline("\n")
					child.expect("#")
					for cmd in cmd_list:
						child.sendline(cmd)
						child.expect("#")
						time.sleep(1)
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + name + " " + ip
			child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			child.logfile = show_result
			child.logfile_read = sys.stdout
			index = child.expect(["assword", pexpect.TIMEOUT])
			if index == 0:
				try:
					child.sendline(pwd)
					child.expect("#")
					child.sendline("config")
					child.sendline("\n")
					child.expect("#")
					for cmd in cmd_list:
						child.sendline(cmd)
						child.expect("#")
						time.sleep(1)
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			error_file = open("error_ip", "w")
			error_file.write(ip)
			error_file.write("#########################")


# save configuration
	#def write_memory

# Terminate the conncetion
	def close_connection(self):
		child.expect("#")
		child.sendline("end")
		child.sendline("exit")			
		child.close()
		show_result.close()








		


