import os.path
import pymysql
import pandas as pd
import numpy as np
import boto3
from smb.SMBConnection import SMBConnection
import socket

def has_element(value,element_list):
    for i in element_list:
        if i in value:
            return True
    return False


def output_collection(date):
    sql_path = "/Users/ziweishi/Downloads/deepviewdata.sql"

    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='szw970727',
        database='dha',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()

    with open(sql_path, 'r') as sql_file:
        sql_statements = sql_file.read().split(';')
        for statement in sql_statements:
            if statement.strip():
                cursor.execute(statement)
    # 提交更改
    connection.commit()

    query1 = "select * from imagecollection_imaging left join wounds_imaging on imagecollection_imaging.WOUNDID = wounds_imaging.WOUNDID left join patient_imaging on wounds_imaging.PID = patient_imaging.PID"
    cursor.execute(query1)
    collection_result = cursor.fetchall()
    df = pd.DataFrame(collection_result)

    path = "../../../Desktop/DHA/latest_dha.xlsx"

    filter = ["555", "7890", "99"]
    # filter = []

    df = df[~df["MedicalNumber"].apply(lambda x: has_element(x, filter))]

    df["source_path"] = df["ImageCollFolderName"].apply(lambda x: x.replace("D:\\ImagingApp\\", "/DHA/NOLABURN/Clean_Truth_Event_NOLA_20230727/"))
    df["source_path"] = df["source_path"].apply(lambda x: x.replace("\\", "/"))
    # df["SubjectID"] = df["MedicalNumber"]
    #
    # df["patient_folder"] = df["ImageCollFolderName"].apply(
    #     lambda x: (x.split("\\"))[2])
    #
    # df["s3_path"] = df["ImageCollFolderName"].apply(lambda x: x.replace("D:\\","DataTransfers/Nola_Burn_Unit/SMD_101_001/"))
    #
    # col = ['ImgCollGUID', 'ImageCollFolderName', 'CreateDateTime', 'AnatomicalLocation', 'SubjectID',
    #        'patient_folder',"s3_path"]

    # df = df[col]

    df["local_path"] = df["ImageCollFolderName"].apply(lambda x: x.replace("D:\\ImagingApp\\", "../../../Desktop/DHA/truthing_images/"))
    df["local_path"] = df["local_path"].apply(lambda x: x.replace("\\", "/"))

    df.to_excel(path)

    cursor.close()
    connection.close()

    return df


def download_pseudo(date):
    a = input("new transfer database?")
    if a != "yes":
        df = pd.read_excel("/Users/ziweishi/Desktop/DHA/new_dha.xlsx")
    else:
        df = output_collection(date)
    folder_path = "/Users/ziweishi/Desktop/DHA/" + date + "/"
    if os.path.isdir(folder_path) == False:
        os.mkdir(folder_path)

    guid = df["ImgCollGUID"].to_list()
    print("total collection num is: " + str(len(guid)))
    s3_path = df["s3_path"].to_list()

    s3 = boto3.resource('s3')
    bucket = s3.Bucket("smddha")

    index=0
    for i in guid:
        guid_path = os.path.join(folder_path,i)
        if os.path.isdir(guid_path) == False:
            os.mkdir(guid_path)
        s3_folder = s3_path[index]
        s3_folder = s3_folder.replace("\\","/")
        index+=1
        s3_list = bucket.objects.filter(Prefix=s3_folder)
        for j in s3_list:
            p = j.key
            if "PseudoColor" in p:
                s3_file = s3_folder+ p
                file_name = s3_file.split("/")[-1]
                file_compo = file_name.split(".")
                file_final = file_compo[0]+"_"+i+"."+file_compo[1]
                local_path =  os.path.join(guid_path,file_final)
                s3.Bucket("smddha").download_file(str(p), str(local_path))
                print(index)




def copy_image(df):
    my_name = socket.gethostname()
    remote_name = 'smd-fs.SpectralMD.com.'
    smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,
                                       is_direct_tcp=True)
    smb_connection.connect("192.168.110.252", 445)
    shared_folder_name = 'Handheld'


    source_list = df["source_path"].to_list()
    local_list = df["local_path"].to_list()
    guid_list = df["ImgCollGUID"].to_list()

    index = 0

    pseudo_list = []
    raw_list = []



    for i in source_list:
        local_path = local_list[index]
        guid = guid_list[index]

        file_list = smb_connection.listPath(shared_folder_name, i)

        p_filter_keywords = ["PseudoColor"]
        p_file_names = [file.filename for file in file_list if any(keyword in file.filename for keyword in p_filter_keywords)]

        r_filter_keywords = []
        r_file_names = [file.filename for file in file_list if
                      any(keyword in file.filename for keyword in r_filter_keywords)]


        file_names = p_file_names+r_file_names



        raw_list.append(r_file_names)

        pseudo_guid = []

        for j in file_names:
            file_path = i+"/"+j
            local_file_folder = "../../../Desktop/DHA/truthing_images/"+ guid+"/"
            if os.path.isdir(local_file_folder) == False:
                os.makedirs(local_file_folder)

            j_list = j.split("_")
            j = j_list[1]+"_"+guid+"_"+j_list[2]+".tif"
            local_file_path = local_file_folder+j

            pseudo_guid.append(j)

            # with open(local_file_path, 'wb') as download_path:
            #     smb_connection.retrieveFile(shared_folder_name, file_path, download_path)
        index+=1
        print(index)

        pseudo_list.append(pseudo_guid)



    df["PseudoColor_List"] = pseudo_list
    # df["RAW_List"] = raw_list

    col = ["IMCOLLID","ImgCollGUID","WOUNDID","ImageCollFolderName","MedicalNumber","source_path","PseudoColor_List"]
    df = df[col]
    df.to_excel("../../../Desktop/DHA/truthing_images/file_path.xlsx")



def truth_image(df):
    my_name = socket.gethostname()
    remote_name = 'smd-fs.SpectralMD.com.'
    smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,
                                       is_direct_tcp=True)
    smb_connection.connect("192.168.110.252", 445)
    shared_folder_name = 'Handheld'
    local_folder = "/Users/ziweishi/Downloads/DHA_Truthing"
    df = df[df["MedicalNumber"]!="101-004"]
    source_list = df["source_path"].to_list()
    guid_list = df["ImgCollGUID"].to_list()
    sub_list = df["MedicalNumber"].to_list()
    wound_list = df["AnatomicalLocation"].to_list()
    index = 0

    pseudo_list = []

    for i in source_list:
        local_patient = local_folder+"/"+sub_list[index]
        wound_suffix = wound_list[index]
        wound_info = wound_suffix.split("_")
        wound = wound_info[0]
        suffix = wound_info[1]
        local_wound = os.listdir(local_patient)
        wound_path = ""
        f_wound = ""
        for w in local_wound:
            if len(w.split("_"))==3:
                if wound in w and suffix in w:
                    wound_path = local_patient + "/" + w
                    f_wound = w
            elif wound in w:
                wound_path = local_patient+"/"+w
                f_wound =w

        print(wound_suffix+" + "+f_wound)
        print(local_wound)


        guid = guid_list[index]
        # print(guid)

        file_list = smb_connection.listPath(shared_folder_name, i)

        p_filter_keywords = ["PseudoColor"]
        p_file_names = [file.filename for file in file_list if any(keyword in file.filename for keyword in p_filter_keywords)]

        file_names = p_file_names

        pseudo_guid = []

        for j in file_names:
            file_path = i+"/"+j
            local_file_folder = wound_path+"/"+guid+"/"
            if os.path.isdir(local_file_folder) == False:
                os.makedirs(local_file_folder)

            j_list = j.split("_")
            j = j_list[1]+"_"+guid+"_"+j_list[2]+".tif"
            local_file_path = local_file_folder+j

            pseudo_guid.append(j)
            with open(local_file_path, 'wb') as download_path:
                smb_connection.retrieveFile(shared_folder_name, file_path, download_path)
        index+=1
        print(index)

        pseudo_list.append(pseudo_guid)














if __name__ == "__main__":
    # download_pseudo("0814")
    # output_collection("0814")

    df = pd.read_excel("/Users/ziweishi/Desktop/DHA/latest_dha.xlsx")
    # copy_image(df)
    truth_image(df)