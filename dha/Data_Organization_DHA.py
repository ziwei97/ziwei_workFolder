import os.path
import shutil
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


def output_collection(sql_path):
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

    path = "DHA_Info.xlsx"

    filter = ["555", "7890", "99"]

    df = df[~df["MedicalNumber"].apply(lambda x: has_element(x, filter))]

    df["source_path"] = df["ImageCollFolderName"].apply(lambda x: x.replace("D:\\ImagingApp\\", "/DHA/NOLABURN/Clean_Truth_Event_NOLA_20230727/"))
    df["source_path"] = df["source_path"].apply(lambda x: x.replace("\\", "/"))



    df["local_path"] = df["ImageCollFolderName"].apply(lambda x: x.replace("D:\\ImagingApp\\", "../../../Desktop/DHA/truthing_images/"))
    df["local_path"] = df["local_path"].apply(lambda x: x.replace("\\", "/"))

    df.to_excel(path)

    cursor.close()
    connection.close()

    return df


def download_pseudo(date):
    a = input("new transfer database?")
    if a == "yes":
        df = output_collection(sql_path="deepviewdata.sql")
    else:
        df = pd.read_excel("DHA_Info.xlsx")
    folder_path = "../DHA_Images/"
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
            local_file_folder = "../DHA_images/"+ guid+"/"
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

    # col = ["IMCOLLID","ImgCollGUID","WOUNDID","ImageCollFolderName","MedicalNumber","source_path","PseudoColor_List"]




def truth_image(df):
    my_name = socket.gethostname()
    remote_name = 'smd-fs.SpectralMD.com.'
    smb_connection = SMBConnection('zshi', "2ntjhy1V1Jrk", my_name, remote_name, use_ntlm_v2=True,
                                       is_direct_tcp=True)
    smb_connection.connect("192.168.110.252", 445)
    shared_folder_name = 'Handheld'
    local_folder = "../DHA_Truthing/NOLA"

    download_folder = "../PatientData/NOLA"
    df = df[df["MedicalNumber"]!="101-004"]
    source_list = df["source_path"].to_list()
    guid_list = df["ImgCollGUID"].to_list()
    sub_list = df["MedicalNumber"].to_list()
    wound_list = df["fix"].to_list()
    index = 0

    pseudo_list = []
    bme_wound = []
    castor_wound = []

    for i in source_list:
        local_patient = local_folder+"/"+sub_list[index]
        download_patient = download_folder+"/"+sub_list[index]
        wound_suffix = wound_list[index]
        if "_" in wound_suffix:
            wound_info = wound_suffix.split("_")
            wound = wound_info[0]
            suffix = wound_info[1]
        else:
            wound = wound_suffix
            suffix = np.nan

        local_wound = os.listdir(local_patient)
        wound_path = ""
        f_wound = ""
        for w in local_wound:
            w_list = w.split("_")
            if len(w_list) == 2:
                if wound in w:
                    wound_path = download_patient + "/" + w
                    f_wound = w
            else:
                if wound in w and suffix in w:
                    wound_path = download_patient + "/" + w
                    f_wound = w



        castor_wound.append(f_wound)
        local_wound1 = [x for x in local_wound if ".DS" not in x]
        bme_wound.append(local_wound1)

        print(wound+" + "+f_wound)
        print(local_wound)


        guid = guid_list[index]
        # print(guid)

        file_list = smb_connection.listPath(shared_folder_name, i)

        p_filter_keywords = ["webcam"]
        p_file_names = [file.filename for file in file_list if any(keyword in file.filename for keyword in p_filter_keywords)]

        file_names = p_file_names



        pseudo_guid = []

        for j in file_names:
            file_path = i+"/"+j
            local_file_folder = wound_path+"/"+guid+"/"
            if os.path.isdir(local_file_folder) == False:
                os.makedirs(local_file_folder)

            # j_list = j.split("_")
            # j = j_list[1]+"_"+guid+"_"+j_list[2]+".tif"
            local_file_path = local_file_folder+j
            pseudo_guid.append(j)
            with open(local_file_path, 'wb') as download_path:
                smb_connection.retrieveFile(shared_folder_name, file_path, download_path)
        index+=1
        print(index)

        pseudo_list.append(pseudo_guid)

    df["BME_Wound"] = bme_wound
    df["Castor_Wound"] = castor_wound

    # col = ["ImgCollGUID","AnatomicalLocation","fix","Castor_Wound","BME_Wound","MedicalNumber","source_path","local_path"]








def match_image(df):
    patient_folder = "../PatientData/NOLA"
    cas_folder = "../DHA_Images/NOLA"
    sub_list = ["101-001","101-002","101-003","101-005","101-006"]


    for s in sub_list:

        df_s = df[df["MedicalNumber"]==s]
        wound_list = df_s["burn_num"].to_list()
        wound_index = []
        for w in wound_list:
            if w not in wound_index:
                wound_index.append(w)
        for index in wound_index:
            df_burn_info = pd.DataFrame()
            df_s_w = df_s[df_s["burn_num"]==index]
            burn = df_s_w["Castor_Wound"].iloc[0]
            guid = df_s_w["ImgCollGUID"].to_list()
            info_subject = []
            info_burn = []
            info_pseudo = []
            info_postbio = []
            info_guid = []
            t_burn_folder = patient_folder + "/" + s + "/" + "Burn" + str(index)

            image_folder = patient_folder + "/" + s + "/" + burn
            biopsy_folder = cas_folder + "/" + s + "/" + burn
            for i in guid:
                file_folder = image_folder + "/" + i
                files = os.listdir(file_folder)
                for f in files:
                    if "PseudoColor" in f:
                        info_subject.append(s)
                        info_burn.append(index)
                        info_pseudo.append(s + "\\" + "BURN" + str(index) + "\\" + "Pseudocolor\\" + f)
                        info_postbio.append(s + "\\" + "BURN" + str(index) + "\\" + "Postbiopsy.JPG")
                        info_guid.append(i)
                        file_path = file_folder + "/" + f
                        t_p_path = t_burn_folder + "/" + "Pseudocolor"
                        if os.path.isdir(t_p_path) == False:
                            os.makedirs(t_p_path)
                        t_p_f_path = t_p_path + "/" + f
                        shutil.copy(file_path, t_p_f_path)
                    if "web" in f:
                        file_path = file_folder + "/" + f
                        t_r_path = t_burn_folder + "/" + "Reference"
                        if os.path.isdir(t_r_path) == False:
                            os.makedirs(t_r_path)
                        t_r_f_path = t_r_path + "/" + f
                        shutil.copy(file_path, t_r_f_path)

            biopsy_list = os.listdir(biopsy_folder)
            for b in biopsy_list:
                if ".DS" not in b:
                    biopsy_path = biopsy_folder + "/" + b
                    t_biopsy_path = t_burn_folder + "/" + b
                    shutil.copy(biopsy_path, t_biopsy_path)

            df_burn_info["Subject"] = info_subject
            df_burn_info["Burn"] = info_burn
            df_burn_info["PseudocolorLocation"] = info_pseudo
            df_burn_info["PostbiopsyLocation"] = info_postbio
            df_burn_info["ImgCollGUID"] = info_guid



            df_info_path = t_burn_folder+"/"+"Table_Burn"+str(index)+".xlsx"
            df_burn_info.to_excel(df_info_path,index=False)































if __name__ == "__main__":
    # download_pseudo("0814")
    # output_collection("0814")

    df = pd.read_excel("/Users/ziweishi/Desktop/DHA_fixed_info.xlsx")
    # copy_image(df)
    # truth_image(df)
    match_image(df)