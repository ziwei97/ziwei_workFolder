from smb.SMBConnection import SMBConnection
import os
from decouple import config
import socket
from datetime import datetime, timedelta
import boto3

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def dfu_sql_find(site_list):
    my_name = socket.gethostname()
    remote_name = 'smd-fs.SpectralMD.com.'
    smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,
                                   is_direct_tcp=True)
    # smb_connection.connect("192.168.110.252", port=445)
    # assert smb_connection.connect("192.168.110.252", 445)
    smb_connection.connect("192.168.110.252", 445)
    info_list={}

    for site in site_list.keys():
        if site_list[site]["type"]=="local":
            try:
                shared_folder_name = 'DFU'
                site_sql_fold = "/DataTransfers/" + site + "/DFU_SS/"
                file_list = smb_connection.listPath(shared_folder_name, site_sql_fold)
                file_names = [file.filename for file in file_list if "." not in file.filename]

                print(file_names)
                max_time = datetime(2020, 1, 1)
                max_file = 0
                tag = 0
                for i in file_names:
                    i = i.replace("-", "_")
                    if "full" in i:
                        max_file = i
                        tag = "full"
                    else:
                        time = i.split("_")
                        year = time[-1]
                        year = "20" + year[-2:]
                        date = time[-2]
                        month = time[-3]
                        date_time = month + "-" + date + "-" + year
                        tag = date_time
                        real_time = datetime.strptime(date_time, '%m-%d-%Y')
                        if real_time > max_time:
                            max_time = real_time
                            max_file = i
                        else:
                            max_time = max_time
                max_sql_fold = site_sql_fold + max_file + "/SpectralView/dvsspdata.sql"
                local_path = "/Users/ziweishi/Documents/transfer_regular_check/sql_file/" + site + "_" + tag + "_dvsspdata.sql"
                with open(local_path, 'wb') as local_file:
                    smb_connection.retrieveFile(shared_folder_name, max_sql_fold, local_file)
                info_list[site] = local_path
            except:
                smb_connection.close()
                info_list[site] = "none"
        else:
            s3_path = "DataTransfer/WAUSI_Connolly_Hospital_Ireland/SMD2211-004/dvsspdata.sql"
            tag = "temp1"
            local_path = "/Users/ziweishi/Documents/transfer_regular_check/latest_sql/" + site + "_" + tag + "_dvsspdata.sql"
            s3.Bucket("spectralmd-uk").download_file(s3_path, local_path)
            info_list[site]=local_path

    smb_connection.close()
    return info_list





    # except:
    #     print("error")
    #     smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,is_direct_tcp=True)
    #     smb_connection.close()








print(dfu_sql_find({"ocer":{"type":"local"}}))


# my_name = socket.gethostname()
# remote_name = 'smd-fs.SpectralMD.com.'
# smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,is_direct_tcp=True)
# smb_connection.close()

