import telnetlib
import subprocess
import threading
from IPy import IP


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
		# ping_able = [{"ping_able:":[]}]
		# ping_unable = {"ping_unable:":[]}
		# self._PING(ip, ping_able["ping_able:"], ping_unable["ping_unable:"])
		# print("ping_able: %s" % ping_able["ping_able:"])
		# print("ping_unable: %s" % ping_unable["ping_unable:"])
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






		


