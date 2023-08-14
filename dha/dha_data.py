import os.path
import pymysql
import pandas as pd
import numpy as np
import boto3

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

    path = "/Users/ziweishi/Desktop/DHA/" + date + "_dha.xlsx"

    filter = ["555", "7890", "99"]

    df = df[~df["MedicalNumber"].apply(lambda x: has_element(x, filter))]

    df["SubjectID"] = df["MedicalNumber"]

    df["patient_folder"] = df["ImageCollFolderName"].apply(
        lambda x: (x.split("\\"))[2])

    df["s3_path"] = df["ImageCollFolderName"].apply(lambda x: x.replace("D:\\","DataTransfers/Nola_Burn_Unit/SMD_101_001/"))

    col = ['ImgCollGUID', 'ImageCollFolderName', 'CreateDateTime', 'AnatomicalLocation', 'SubjectID',
           'patient_folder',"s3_path"]

    df = df[col]
    df.to_excel(path)

    df_latest = df
    df_latest.to_excel("/Users/ziweishi/Desktop/DHA/new_dha.xlsx")

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


# if __name__ == "__main__":
    # download_pseudo("0814")
    # output_collection("0814")