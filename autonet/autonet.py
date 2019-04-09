import telnetlib
import subprocess
import threading
import pexpect
import getpass
import sys
import re
import time
from IPy import IP


class AutoNet(object):

	def __init__(self, username, device_ios, url=" ", url_error_ip=" "):
		self.username = username
		self.password = getpass.getpass("Pls input your password:")
		self.device_ios = device_ios
		self.result_file = open(url, "w")
		self.error_file = open(url_error_ip, "w")
		__child = ""


#check reachibility
	def __PING(self, ip, ping_able, ping_unable):
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
		self.__PING(ip, ping_able, ping_unable)
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
			t = threading.Thread(target=self.__PING, args=(str(ip),ping_able,ping_unable,))
			threads.append(t)

		for i in range(len(threads)):
			threads[i].start()

		for i in range(len(threads)):
			threads[i].join()
		ping_result["ping_able:"] = ping_able
		ping_result["ping_unable:"] = ping_unable
		return(ping_result)

# show command via telnet or ssh
	def auto_show(self, ip, cmd):
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip	
			self.__child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			self.__child.logfile = self.result_file
			self.__child.logfile_read = sys.stdout
			index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				self.__child.sendline(self.username)
				self.__child.expect("assword")
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("ter len 0")
					self.__child.expect("#")
					self.__child.sendline(cmd)
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + self.username+ " " + ip
			self.__child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			self.__child.logfile = self.result_file
			self.__child.logfile_read = sys.stdout
			index = self.__child.expect(["assword", "yes/no", pexpect.TIMEOUT])
			if index == 0:
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("ter len 0")
					self.__child.expect("#")
					self.__child.sendline(cmd)
				except Exception as e:
					print(e)
			elif index == 1:
				try:
					self.__child.sendline("yes")
					self.__child.expect("assword")
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("ter len 0")
					self.__child.expect("#")
					self.__child.sendline(cmd)
				except Exception as e:
					print(e)				
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			print("Pls check the %s or command and try again :(" % ip)
			self.error_file.write(ip)
			self.error_file.write("\n")
			self.error_file.write("#########################")


# download configuration with single cmd
	def auto_config(self, ip, cmd):
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip
			self.__child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			self.__child.logfile = self.result_file
			self.__child.logfile_read = sys.stdout
			index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				self.__child.sendline(self.username)
				self.__child.expect("assword")
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("config")
					self.__child.sendline("\n")
					self.__child.expect("#")
					self.__child.sendline(cmd)
					self.__child.expect("#")
					self.__child.sendline("end")
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + self.username + " " + ip
			self.__child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			self.__child.logfile = self.result_file
			self.__child.logfile_read = sys.stdout
			index = self.__child.expect(["assword", pexpect.TIMEOUT])
			if index == 0:
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("config")
					self.__child.sendline("\n")
					self.__child.expect("#")
					self.__child.sendline(cmd)
					self.__child.expect("#")
					self.__child.sendline("end")
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			print("Pls check the %s or command and try again:(" % ip)
			self.error_file.write(ip)
			self.error_file.write("\n")
			self.error_file.write("#########################")


# download configuration from file
	def auto_config_file(self, ip, file):
		cmd_list =[]
		cmd_file = open(file)
		for i in cmd_file:
			cmd_list.append(re.sub("\n", "", i))
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip
			self.__child = pexpect.spawn(cmd_login_telnet, timeout=3, encoding='utf-8')
			self.__child.logfile = self.result_file
			self.__child.logfile_read = sys.stdout
			index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				self.__child.sendline(self.username)
				self.__child.expect("assword")
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("config")
					self.__child.sendline("\n")
					self.__child.expect("#")
					for cmd in cmd_list:
						self.__child.sendline(cmd)
						self.__child.expect("#")
						time.sleep(1)
					self.__child.expect("#")
					self.__child.sendline("end")
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + self.username+ " " + ip
			self.__child = pexpect.spawn(cmd_login_ssh, timeout=3,encoding='utf-8')
			self.__child.logfile = self.result_file
			self.__child.logfile_read = sys.stdout
			index = self.__child.expect(["assword", pexpect.TIMEOUT])
			if index == 0:
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("config")
					self.__child.sendline("\n")
					self.__child.expect("#")
					for cmd in cmd_list:
						self.__child.sendline(cmd)
						self.__child.expect("#")
						time.sleep(1)
					self.__child.expect("#")
					self.__child.sendline("end")
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			print("Pls check the %s or command and try again:(" % ip)
			self.error_file.write(ip)
			self.error_file.write("\n")
			self.error_file.write("#########################")


# save configuration
	def write_memory(self):
		self.__child.expect("#")
		if self.device_ios == "ios":
			self.__child.sendline("write")
			time.sleep(1)
		elif self.device_ios == "nxos":
			self.__child.sendline("copy runn start")
			time.sleep(1)



# Terminate the conncetion
	def close_connection(self):
		try:
			self.__child.expect("#")
			self.__child.sendline("exit")			
			self.__child.close()
			self.result_file.close()
		except:
			self.error_file.close()








		


