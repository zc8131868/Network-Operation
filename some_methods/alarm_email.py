import schedule
import datetime
import time
import smtplib
import autonet_2019_0513
import getpass
import re
from email.mime.text import MIMEText
from threading import Timer


global pwd, pwd_email
count = 0
pwd = getpass.getpass("pls input your password:")
pwd_email = getpass.getpass("pls input the password for your email account:")

def BGP_Neighbor(ip):

	HOST = "smtp.gmail.com"
	TO = "zc8131868@gmail.com"
	FROM = "zc8131868@gmail.com"
	SUBJECT = "BGP neighbor status"

	a = autonet_2019_0513.autonet(username="chengzheng",
						password=pwd,
						device_ios="cisco_nxos",
						url="/Users/zhengcheng/Desktop/result.txt",
						url_error_ip="/Users/zhengcheng/Desktop/error_ip.txt"
						)	
	a.auto_show(ip, "show ip bgp summ")
	a.close_logging()

	with open("/Users/zhengcheng/Desktop/result.txt") as f:
		content = f.read()

	# if re.findall("Active|Connect|Idle", content) != []:
	if re.findall("37963", content) != []:	
		t = datetime.datetime.now().strftime("%H:%M:%S %m-%d-%Y")
		TEXT = "\n#################################################\n".join((t, content))
		msg = MIMEText(TEXT, "plain")
		msg["from"] = FROM
		msg["to"] = TO
		msg["subject"] = SUBJECT

		server = smtplib.SMTP(HOST)
		server.connect(HOST, 587)
		server.starttls()
		server.login("zc8131868@gmail.com", pwd_email)
		server.sendmail(FROM, TO, msg.as_string())
		server.quit()
	else:
		pass
	global count
	print("############################################\n")
	print(count)
	count = count + 1
	t_BGP_Neighbor = Timer(30, BGP_Neighbor, [ip])
	t_BGP_Neighbor.start()
	if count > 4:
		t_BGP_Neighbor.cancel()


def Reachability():

		HOST = "smtp.gmail.com"
		TO = "zc8131868@gmail.com"
		FROM = "zc8131868@gmail.com"
		SUBJECT = "Unreachable IP"

		a = autonet_2019_0513.autonet(username="chengzheng",
						password=pwd,
						device_ios="cisco_nxos",
						url="/Users/zhengcheng/Desktop/result.txt",
						url_error_ip="/Users/zhengcheng/Desktop/error_ip.txt"
						)

		res = a.PING_IP(["30.26.0.6", "30.26.0.2"])
		unre_ip = res["unreachable"]

		if unre_ip != []:
			t = datetime.datetime.now().strftime("%H:%M:%S %m-%d-%Y")
			TEXT = "\n".join((t, str(unre_ip)))
			msg = MIMEText(TEXT, "plain")
			msg["from"] = FROM
			msg["to"] = TO
			msg["subject"] = SUBJECT

			server = smtplib.SMTP(HOST)
			server.connect(HOST, 587)
			server.starttls()
			server.login("zc8131868@gmail.com", pwd_email)
			server.sendmail(FROM, TO, msg.as_string())
			server.quit()
		else:
			pass
		t_Reachability = Timer(60, Reachability)

		return(t_Reachability)

def alarm_email():
	threads = []
	ip_set = ["30.25.0.255"]
	for ip in ip_set:
		threads.append(Timer(30, BGP_Neighbor, [ip]))

	for i in range(len(threads)):
		threads[i].start()
		# print(count)
		# if count > 4:
		# 	threads[i].cancel()

	# for i in range(len(threads)):
	# 	threads[i].join()

alarm_email()


