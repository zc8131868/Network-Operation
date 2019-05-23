Hello, Network-Operation is aimed at providing some tools or modules for network automated operation.
If you are interested in it, find bugs or have any requirement, feel free to contact me via zc8131868@gmail.com.
You may also find more useful methods in some_methods folder.
For more details please check examples.docx for reference.



import getpass

pwd = getpass.getpass("pls input your password::")

a = autonet.autonet(username="chengzheng", 
					          password = pwd,
					          device_ios= "cisco_ios", 
					          url="/Users/zhengcheng/Desktop/result.txt", 
					          url_error_ip="/Users/zhengcheng/Desktop/error_ip.txt"
				          	)
  
b = a.PING_IP(["1.1.1.1", "2.2.2.2)]
b = a.PING_Subnet("1.1.1.0/24")
b = a.get_version("30.31.190.94")
b = a.get_serial_number("30.31.190.94")
a.auto_show("1.1.1.1", "show ntp status")
a.auto_config("2.2.2.2", ["hostname test", "interface g0/1", "switchport mode trunk"])
a.auto_config_file("1.1.1.1", "commands.txt")
a.close_logging()

For now, autonet has been tested on cisco_ios, cisco_nxos, rg_os. It's no double other OS can use PING_IP or PING_Subnet which is independent on OS command. Autnonet will support more OS later.





