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


class autonet(object):

	def __init__(self, username, password="", device_ios="cisco_ios", url=" ", url_error_ip=" "):
		self.username = username
		self.device_ios = device_ios
		self.result_file = open(url, "w")
		self.error_file = open(url_error_ip, "w")
		__child = ""
		if password == "":
			self.password = getpass.getpass("Pls input your password:")
		else:
			self.password = password



#check reachibility
	def __PING(self, ip, reachable, unreachable):
		try:
			subprocess.check_call('ping -c 1 %s' %ip, shell=True)
			reachable.append(ip)
		except Exception as e:
			unreachable.append(ip)

#check reachibility of given ip address
	def PING_IP(self,ip):
		reachable = []
		unreachable = []
		threads = []
		ping_result = {"reachable":reachable, "unreachable":unreachable}
		for i in ip:
			t = threading.Thread(target=self.__PING, args=(i,reachable,unreachable))
			threads.append(t)

		for i in range(len(threads)):
			threads[i].start()

		for i in range(len(threads)):
			threads[i].join()

		return(ping_result)

# check reachibility of ip addresses of given subnet
	def PING_Subnet(self, subnet):
		reachable = []
		unreachable = []
		ping_result = {"reachable":reachable, "unreachable":unreachable}
		threads = []
		subnet = IP(subnet)
		for ip in subnet:
			t = threading.Thread(target=self.__PING, args=(str(ip),reachable,unreachable))
			threads.append(t)

		for i in range(len(threads)):
			threads[i].start()

		for i in range(len(threads)):
			threads[i].join()

		return(ping_result)

# show command via telnet or ssh
	def auto_show(self, ip, cmd):
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip	
			self.__child = pexpect.spawn(cmd_login_telnet, timeout=5, encoding='utf-8')
			self.__child.logfile_read = self.result_file
			self.__child.logfile = sys.stdout
			index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				self.__child.sendline(self.username)
				self.__child.expect("assword")
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("ter len 0")
					self.__child.expect("#")
					for c in cmd:
						self.__child.sendline(c)
						self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username and password")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + self.username+ " " + ip
			self.__child = pexpect.spawn(cmd_login_ssh, timeout=5, encoding='utf-8')
			self.__child.logfile_read = self.result_file
			self.__child.logfile = sys.stdout
			index = self.__child.expect(["assword", "yes/no", pexpect.TIMEOUT])
			if index == 0:
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					self.__child.sendline("ter len 0")
					self.__child.expect("#")
					for c in cmd:
						self.__child.sendline(c)
						self.__child.expect("#")
					self.__child.sendline("exit")
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
					for c in cmd:
						self.__child.sendline(c)
						self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print(e)				
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			print("Pls check %s or command and try again" % ip)
			self.error_file.write(ip)
			self.error_file.write("\n")
			self.error_file.write("#########################")


# download configuration with given cmd
	def auto_config(self, ip, cmd):
		try:
			telnetlib.Telnet(ip, 23, 5)
			cmd_login_telnet = "telnet " + ip
			self.__child = pexpect.spawn(cmd_login_telnet, timeout=20, encoding='utf-8')
			self.__child.logfile_read = self.result_file
			self.__child.logfile = sys.stdout
			index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				self.__child.sendline(self.username)
				self.__child.expect("assword")
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					if self.device_ios == "cisco_ios":
						self.__child.sendline("config t")
					else:
						self.__child.sendline("config")
					self.__child.expect("#")
					for c in cmd:
						self.__child.sendline(c)
						self.__child.expect("#")
					self.__child.sendline("end")
					self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + self.username + " " + ip
			self.__child = pexpect.spawn(cmd_login_ssh, timeout=20, encoding='utf-8')
			self.__child.logfile_read = self.result_file
			self.__child.logfile = sys.stdout
			index = self.__child.expect(["assword", "yes/no", pexpect.TIMEOUT])
			if index == 0:
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					if self.device_ios == "cisco_ios":
						self.__child.sendline("config t")
					else:
						self.__child.sendline("config")
					self.__child.expect("#")
					for c in cmd:
						self.__child.sendline(c)
						self.__child.expect("#")
					self.__child.sendline("end")
					self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username or password again")
			elif index == 1:
				try:
					self.__child.sendline("yes")
					self.__child.expect("assword")					
					self.__child.sendline(self.password)
					self.__child.expect("#")
					if self.device_ios == "cisco_ios":
						self.__child.sendline("config t")
					else:
						self.__child.sendline("config")
					self.__child.expect("#")
					for c in cmd:
						self.__child.sendline(c)
						self.__child.expect("#")
					self.__child.sendline("end")
					self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username or password again")								
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			print("Pls check %s or command and try again" % ip)
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
			self.__child = pexpect.spawn(cmd_login_telnet, timeout=20, encoding='utf-8')
			self.__child.logfile_read = self.result_file
			self.__child.logfile = sys.stdout
			index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
			if index == 0 or index == 1:
				self.__child.sendline(self.username)
				self.__child.expect("assword")
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					if self.device_ios == "cisco_ios":
						self.__child.sendline("config t")
					else:
						self.__child.sendline("config")
					self.__child.expect("#")
					for cmd in cmd_list:
						self.__child.sendline(cmd)
						self.__child.expect("#")
					self.__child.sendline("end")
					self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username or password again")
			else:
				print("Cannot telnet this ip address %s" % ip)

		except ConnectionRefusedError:
			cmd_login_ssh = "ssh -l " + self.username+ " " + ip
			self.__child = pexpect.spawn(cmd_login_ssh, timeout=20, encoding='utf-8')
			self.__child.logfile_read = self.result_file
			self.__child.logfile = sys.stdout
			index = self.__child.expect(["assword", "yes/no", pexpect.TIMEOUT])
			if index == 0:
				try:
					self.__child.sendline(self.password)
					self.__child.expect("#")
					if self.device_ios == "cisco_ios":
						self.__child.sendline("config t")
					else:					
						self.__child.sendline("config")
					self.__child.expect("#")
					for cmd in cmd_list:
						self.__child.sendline(cmd)
						self.__child.expect("#")
					self.__child.sendline("end")
					self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username or password again")
			elif index == 1:
				try:
					self.__child.sendline("yes")
					self.__child.expect("assword")					
					self.__child.sendline(self.password)
					self.__child.expect("#")
					if self.device_ios == "cisco_ios":
						self.__child.sendline("config t")
					else:					
						self.__child.sendline("config")
					self.__child.expect("#")
					for cmd in cmd_list:
						self.__child.sendline(cmd)
						self.__child.expect("#")
					self.__child.sendline("end")
					self.__child.expect("#")
					self.__child.sendline("exit")
				except Exception as e:
					print("check username or password again")				
			else:
				print("Cannot ssh this ip address %s" % ip)
		except:
			print("Pls check %s or command and try again" % ip)
			self.error_file.write(ip)
			self.error_file.write("\n")
			self.error_file.write("#########################")

# close log
	def close_logging(self):	
		self.__child.close()
		self.result_file.close()
		self.error_file.close()	
	
# Get chassis serial number
	def get_serial_number(self, ip):
		with open("sn_log.txt", "w+") as original_file:
			try:
				telnetlib.Telnet(ip, 23, 5)
				cmd_login_telnet = "telnet " + ip
				self.__child = pexpect.spawn(cmd_login_telnet, timeout=20, encoding="utf-8")
				self.__child.logfile_read = original_file
				self.__child.logfile = sys.stdout
				index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
				if index == 0 or index == 1:
					self.__child.sendline(self.username)
					self.__child.expect("assword")
					try:
						self.__child.sendline(self.password)
						self.__child.expect("#")
						if self.device_ios == "cisco_nxos":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show sprom backplane 1")
						elif self.device_ios == "cisco_ios":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						elif self.device_ios == "rg_os":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show ver")
						self.__child.expect("#")
						self.sendline("exit")
					except Exception as e:
						print("check username or password again")
				else:
					print("Cannot tlenet this ip address %s" % ip)

				original_file.seek(0)

				if self.device_ios == "cisco_nxos":
					sn = methodlib.cisco_nxos_sn(original_file)
				elif self.device_ios == "cisco_ios":
					sn = methodlib.cisco_ios_sn(original_file)
				elif self.device_ios == "rg_os":
					sn = methodlib.rg_os_sn(original_file)
				return(sn)

			except ConnectionRefusedError:
				cmd_login_ssh = "ssh -l "+ self.username + " " + ip
				self.__child = pexpect.spawn(cmd_login_ssh, timeout=20, encoding="utf-8")
				self.__child.logfile_read = original_file
				self.__child.logfile = sys.stdout
				index = self.__child.expect(["assword", "yes/no", pexpect.TIMEOUT])
				if index == 0:
					try:
						self.__child.sendline(self.password)
						self.__child.expect("#")
						if self.device_ios == "cisco_nxos":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show sprom backplane 1")
						elif self.device_ios == "cisco_ios":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						elif self.device_ios == "rg_os":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						self.__child.expect("#")
						self.__child.sendline("exit")
					except Exception as e:
						print(e)
				elif index == 1:
					try:
						self.__child.sendline("yes")
						self.__child.expect("assword")
						self.__child.sendline(self.password)
						self.__child.expect("#")
						if self.device_ios == "cisco_nxos":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show sprom backplane 1")
						elif self.device_ios == "cisco_ios":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						elif self.device_ios == "rg_os":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						self.__child.expect("#")
						self.__child.sendline("exit")
					except Exception as e:
						print(e)
				else:
					print("Cannot ssh this ip address %s" % ip)

				original_file.seek(0)

				if self.device_ios == "cisco_nxos":
					sn = methodlib.cisco_nxos_sn(original_file)
				elif self.device_ios == "cisco_ios":
					sn = methodlib.cisco_ios_sn(original_file)
				elif self.device_ios == "rg_os":
					sn = methodlib.rg_os_sn(original_file)
				return(sn)

			except:
				print("Pls check %s or command and try again" % ip)
				self.error_file.write(ip)
				self.error_file.write("\n")
				self.error_file.write("#########################")				



# Get software version
	def get_version(self, ip):
		with open("soft_version.txt", "w+") as original_file:
			try:
				telnetlib.Telnet(ip, 23, 5)
				cmd_login_telnet = "telnet " + ip
				self.__child = pexpect.spawn(cmd_login_telnet, timeout=20, encoding="utf-8")
				self.__child.logfile_read = original_file
				index = self.__child.expect(["username", "login", pexpect.TIMEOUT])
				if index == 0 or index == 1:
					self.__child.sendline(self.username)
					self.__child.expect("assword")
					try:
						self.__child.sendline(self.password)
						self.__child.expect("#")
						if self.device_ios == "cisco_nxos" or self.device_ios == "cisco_ios" or self.device_ios == "rg_os":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						else:
							print("Pls check device_ios")
						self.__child.expect("#")
						self.__child.sendline("exit")
					except Exception as e:
						print("check username or password again")
				else:
					print("Cannot telnet this ip address %s" % ip)

				original_file.seek(0)

				if self.device_ios == "cisco_nxos":
					sv = methodlib.cisco_nxos_sv(original_file)
				elif self.device_ios == "cisco_ios":
					sv = methodlib.cisco_ios_sv(original_file)
				elif self.device_ios == "rg_os":
					sv = methodlib.rg_os_sv(original_file)
				return(sv)

			except ConnectionRefusedError:
				cmd_login_ssh = "ssh -l " + self.username+ " " + ip
				self.__child = pexpect.spawn(cmd_login_ssh, timeout=20, encoding='utf-8')
				self.__child.logfile_read = original_file
				index = self.__child.expect(["assword", "yes/no", pexpect.TIMEOUT])
				if index == 0:
					try:
						self.__child.sendline(self.password)
						self.__child.expect("#")
						if self.device_ios == "cisco_nxos" or self.device_ios == "cisco_ios" or self.device_ios == "rg_os":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						else:
							print("Pls check device_ios")
						self.__child.expect("#")
						self.__child.sendline("exit")
					except Exception as e:
						print(e)
				elif index == 1:
					try:
						self.__child.sendline("yes")
						self.__child.expect("assword")
						self.__child.sendline(self.password)
						self.__child.expect("#")
						if self.device_ios == "cisco_nxos" or self.device_ios == "cisco_ios" or self.device_ios == "rg_os":
							self.__child.sendline("ter len 0")
							self.__child.expect("#")
							self.__child.sendline("show version")
						else:
							print("Pls check device_ios")
						self.__child.expect("#")
						self.__child.sendline("exit")
					except Exception as e:
						print(e)						
				else:
					print("Cannot ssh this ip address %s" % ip)	

				original_file.seek(0)

				if self.device_ios == "cisco_nxos":
					sv = methodlib.cisco_nxos_sv(original_file)
				elif self.device_ios == "cisco_ios":
					sv = methodlib.cisco_ios_sv(original_file)
				elif self.device_ios == "rg_os":
					sv = methodlib.rg_os_sv(original_file)
				return(sv)

			except:
				print("Pls check %s or command and try again" % ip)
				self.error_file.write(ip)
				self.error_file.write("\n")
				self.error_file.write("#########################")	


		


