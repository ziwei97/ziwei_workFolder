from smb.SMBConnection import SMBConnection
import os
import socket
from datetime import datetime
import boto3
import shutil

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def dfu_sql_find(site_list):
    sql_path = "../Documents/dfu_transfer_sql/latest_sql_file/"
    # path = "/Users/ziweishi/Documents/transfer_regular_check/0_sql_file/"
    cur_list = os.listdir(sql_path)
    cur_info_list = {}

    if len(cur_list) > 0:
        cur_list = [x for x in cur_list]
        if ".DS_Store" in cur_list:
            cur_list.remove(".DS_Store")
        for sql in cur_list:
            info = sql.split("_")
            site = info[0]
            cur_info_list[site] = sql_path + sql

    z = input("get latest sql file for each site?")

    if z =="yes":
        shutil.rmtree(sql_path)
        my_name = socket.gethostname()
        remote_name = 'smd-fs.SpectralMD.com.'
        smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,
                                       is_direct_tcp=True)
        # smb_connection.connect("192.168.110.252", port=445)
        # assert smb_connection.connect("192.168.110.252", 445)
        smb_connection.connect("192.168.110.252", 445)
        info_list = {}
        for site in site_list.keys():
            path = sql_path
            if os.path.isdir(path) == False:
                # shutil.rmtree(path)
                os.mkdir(path)
            if site_list[site]["type"] == "local":
                try:
                    shared_folder_name = 'DFU'
                    site_sql_fold = "/DataTransfers/" + site + "/DFU_SS/"
                    file_list = smb_connection.listPath(shared_folder_name, site_sql_fold)
                    filter_keywords = [".", "with", "Mock"]
                    file_names = [file.filename for file in file_list if
                                  all(keyword not in file.filename for keyword in filter_keywords)]
                    max_time = datetime(2020, 1, 1)
                    max_file = 0
                    tag = ""
                    for i in file_names:
                        a = i.replace("-", "_")
                        if "full" in a:
                            max_file = i
                            tag = "full"
                            break
                        else:
                            time = a.split("_")
                            year = time[-1]
                            year = "20" + year[-2:]
                            date = time[-2]
                            month = time[-3]
                            date_time = month + "-" + date + "-" + year
                            real_time = datetime.strptime(date_time, '%m-%d-%Y')
                            if real_time > max_time:
                                max_time = real_time
                                max_file = i
                                tag = date_time
                            else:
                                max_time = max_time
                    max_sql_fold = site_sql_fold + max_file + "/SpectralView/dvsspdata.sql"

                    local_path = path+ site + "_" + tag + "_dvsspdata.sql"
                    with open(local_path, 'wb') as local_file:
                        smb_connection.retrieveFile(shared_folder_name, max_sql_fold, local_file)
                    info_list[site] = local_path
                    print(local_path)
                except:
                    info_list[site] = "none"
            else:
                s3_path = "DataTransfer/WAUSI_Connolly_Hospital_Ireland/CONNOLLY_DFU_SMD2211-004_12_09_23/SpectralView/dvsspdata_revise.sql"
                tag = "temp3"
                local_path = path+ site + "_" + tag + "_dvsspdata.sql"
                s3.Bucket("spectralmd-uk").download_file(s3_path, local_path)
                info_list[site] = local_path
        smb_connection.close()
        print("q1")
        return info_list,z
    else:
        info_list = {}
        for i in site_list:
            info_list[i] = cur_info_list[i]

        return info_list, z


if __name__ == "__main__":
    print(dfu_sql_find({'rsci': {'type': 's3'}}))
