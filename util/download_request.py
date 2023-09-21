import boto3
import os
import numpy as np
import pandas as pd
import random
import pathlib
import cv2
import shutil

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

def parse_date(x):
    try:
        stamp = int(x) - 2209031999999999700 - 6*60*60*1000000000
        eval = str(pd.to_datetime(stamp).strftime('%d-%m-%Y'))
    except:
        eval = np.nan
    return eval

#get attributes from dynamodb
def get_attribute(table,guid,attr):
    try:
        response = table.get_item(
            Key={
                'ImgCollGUID': guid
            }
        )
        # print(response)
        return response["Item"][attr]
    except:
        return  np.nan


def download_raw(table,raw_list,attrs,path):
    index=1
    error_list=[]
    fold = path
    if os.path.isdir(fold) == False:
        os.makedirs(fold)
    else:
        shutil.rmtree(fold)

    # id_list=[]
    # size_list=[]
    # mask_list=[]
    for i in raw_list:
        print(index)
        name = get_attribute(table,i,"Bucket")
        # subject = get_attribute(table, i, "SubjectID")
        # wound = get_attribute(table, i, "Wound")

        # sub = get_attribute(table, i, "SubjectID")
        # sub_folder = os.path.join(fold,subject)
        # if os.path.isdir(sub_folder) == False:
        #     os.mkdir(sub_folder)
        guid_folder = os.path.join(fold, i)
        if os.path.isdir(guid_folder) == False:
            os.mkdir(guid_folder)

        # wound_folder = os.path.join(sub_folder,wound)
        # if os.path.isdir(wound_folder) == False:
        #     os.mkdir(wound_folder)

        # guid_folder = os.path.join(wound_folder,i)
        # os.mkdir(guid_folder)

        for j in attrs:
            try:
                # if j=="PseudoColor":
                #     s = "PseudoColor/PseudoColor_" + str(i) + ".tif"
                #     file_name = "PseudoColor_" + str(i) + ".tif"
                #     file_path = os.path.join(guid_folder, file_name)
                #     s3.Bucket(name).download_file(s, str(file_path))

                # if j=="PrimaryDoctorTruth":
                #     attr = get_attribute(table, i, j)
                #     for s in attr:
                #         file_name = s.split('/')[-1]
                #         file_name1 = "Primary_" + file_name
                #         file_path = os.path.join(guid_folder, file_name1)
                #         s3.Bucket(name).download_file(s, str(file_path))
                #
                # if j=="SecondaryDoctorTruth":
                #     attr = get_attribute(table, i, j)
                #     for s in attr:
                #         file_name = s.split('/')[-1]
                #         file_name1 = "Secondary_" + file_name
                #         file_path = os.path.join(guid_folder, file_name1)
                #         s3.Bucket(name).download_file(s, str(file_path))

                # else:
                    attr = get_attribute(table, i, j)
                    for s in attr:
                        file_name = s.split('/')[-1]
                        file_path = os.path.join(guid_folder, file_name)
                        s3.Bucket(name).download_file(str(s), str(file_path))
                        # img = cv2.imread(file_path)
                        # sp = img.shape
                        # id_list.append(i)
                        # size_list.append(sp)
                        # mask_list.append(file_name)
                        # print(sp)
            except:
                error_list.append(i)
                print(i+" "+j+" Missing")
        index+=1

    # data = zip(id_list,mask_list,size_list)
    # final = pd.DataFrame(data,columns=["GUID","Mask","Size"])
    # final.to_excel("/Users/ziweishi/Desktop/epoc_mask_size.xlsx")

def simple_download(table,guid,attrs,path):
    raw_list = guid.split("\n")
    download_raw(table,raw_list,attrs,path)


def replace_all(text,reo):
    for i in reo:
        if i in text:
            text.replace("i","")
    return text


if __name__ == "__main__":
    # path = "/Users/ziweishi/Documents/database/DFU_Master_ImageCollections.xlsx"
    # df = pd.read_excel(path)
    # sub_name=["201-011","202-035","202-036"]
    # df = df[df["SubjectID"].isin(sub_name)]
    # raw_list = df["ImgCollGUID"].to_list()

    attrs=["PseudoColor","Raw"]

    cor = """3c53f28f-80e7-46f6-9e31-9d0080bf4868
637f44e1-77b8-4837-a4e1-4c47b3dfb6d3
52d101ed-c098-4e42-965d-09acd7bd8df8
0e7d246a-6df2-4d36-99e9-fda5e4e90a2c"""

    path = "/Users/ziweishi/Downloads/Calibration_3D_Measurement/Large_Ulcer"

    raw_list = cor.split("\n")
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    download_raw(table,raw_list,attrs,path)

    # for i in raw_list:
    #     a = get_attribute(table, i, "CreateTimeStamp")
    #     b = get_attribute(table,i,"DeviceID")
    #     print("'" + str(parse_date(a)) + "'")




























