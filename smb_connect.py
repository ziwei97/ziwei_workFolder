from smb.SMBConnection import SMBConnection
from smb.SMBConnection import *


host = "192.168.110.252"
username = "zshi" #用户名，改成你自己的
password = "2ntjhy1V1Jrk" #密码，改成你自己的
my_name = "" # 这个随便，可以为空字符串
remote_name = "" # 这个是共享主机的主机名，listShares会用到，不用listShares的话可以为空字符串
conn = SMBConnection(username, password,my_name, remote_name, use_ntlm_v2=False)
connected = conn.connect(host,445) #smb协议默认端口445
if connected:
    print("success")

