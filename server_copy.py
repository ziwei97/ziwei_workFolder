import os
import paramiko
import pandas as pd

def RemoteScp(host_ip, host_port, host_username, host_password, remote_path, local_path):
    scp = paramiko.Transport((host_ip, host_port))
    scp.connect(username=host_username, password=host_password)
    sftp = paramiko.SFTPClient.from_transport(scp)
    # sftp.mkdir(test_path)
    # sftp.rmdir(test_path)
    df = pd.read_excel("/Users/ziweishi/Desktop/epoc_mask_size.xlsx")
    guid = df["GUID"].to_list()
    index=0
    for i in guid:
        remote_file = remote_path+i+"/Mask_"+i+".png"
        local_file = local_path+"Mask_"+i+".png"
        try:
            sftp.get(remote_file, local_file)
        except IOError:  # 如果目录不存在则抛出异常
            print(i)
            return ("remote_path or local_path is not exist")
        print(index)
        index+=1
    scp.close()


if __name__ == '__main__':
    host_ip = '192.168.110.47'        # 远程服务器IP
    host_port = 22                   # 远程服务器端口
    host_username = 'smd'           #远程服务器用户名
    host_password = 'Texas512'       #远程服务器密码
    remote_path = '/mnt/data/data_engineering/ePOC_raw_data/ePOC_data/'            #这个是远程目录
    local_path = '/Users/ziweishi/Desktop/epoc_mask/'             #这个是本地目录
    RemoteScp(host_ip, host_port, host_username, host_password, remote_path, local_path)  #调用方法
