from smb.SMBConnection import SMBConnection

def smb_connection(username, password, client_name, server_name):
    smb_conn = SMBConnection(username, password, client_name, server_name)
    if smb_conn.connect(server_name, 22):
        file_list = smb_conn.listPath('dfu/DataTransfers', '/')
        for file in file_list:
            print(file.filename)
        smb_conn.close()
    else:
        print('无法连接到SMB服务器')

username = "zshi"
password = "2ntjhy1V1Jrk"
server_name = "192.168.110.252"
smb_connection(username, password, 'localhost', server_name)




