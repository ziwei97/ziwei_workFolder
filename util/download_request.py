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
        os.mkdir(fold)
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
        # guid_folder = os.path.join(sub_folder, i)
        # if os.path.isdir(guid_folder) == False:
        #     os.mkdir(guid_folder)

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
                    guid_folder = os.path.join(fold,j)
                    if os.path.isdir(guid_folder) == False:
                        os.mkdir(guid_folder)
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

    attrs=["DeviceID"]

    cor = """3d0ad712-6e9c-494e-be71-9371ad0ec895
828cf35c-d83d-483c-b6a5-e2034c6e532e
a5683eb8-7998-4b31-afe2-754660ef54d1
495e2767-7e4c-465e-aa14-ee2831dcae2d
15eb17da-561a-4414-91a8-580b172739b1
6d76832a-ed2d-4bcd-868d-bf82f4f51733
6eb1b0b2-23e2-4359-bdbc-e6c1292e32bf
1647e48b-de74-4b48-b2bb-b79f1ac88d41
1666955f-0156-4785-bc72-f0ae036a2964
4e9fb446-7a4c-41b7-9185-3f14f832ce59
5659c7cb-81c8-475d-b772-bcc7031e0a8b
23b0a82e-d35b-4c96-a343-8c9b2732a25c"""

    path = "/Users/ziweishi/Documents/check/"

    raw_list = cor.split("\n")
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    #
    # download_raw(table,raw_list,attrs,path)

    for i in raw_list:
        a = get_attribute(table,i,"CreateTimeStamp")
        print("'"+str(parse_date(a))+"'")























