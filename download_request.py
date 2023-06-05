import boto3
import os
import numpy as np
import pandas as pd
import random
import pathlib
import cv2

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')



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

    # id_list=[]
    # size_list=[]
    # mask_list=[]
    for i in raw_list:
        print(index)
        name = get_attribute(table,i,"Bucket")
        # subject = get_attribute(table, i, "SubjectID")
        # wound = get_attribute(table, i, "Wound")
        # sub_folder = os.path.join(fold,subject)
        guid_folder = os.path.join(fold,i)
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
                print(i)
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


    path = "/Users/ziweishi/Desktop/dfu.xlsx"
    df = pd.read_excel(path,sheet_name="Sheet2")
    raw_list_og = df["ImgCollGUID"].to_list()
    raw_list = raw_list_og[1252:]
    # raw_list1 = raw_list_og[0:134]

#     raw_list ="""aeff569f-d617-4303-8786-67f13217554a
# 52118b78-4a33-4a99-b289-6da59e5031d3
# 03c446e7-de05-42aa-bd5d-1ae2728c7729
# a2863b2c-552c-495c-b3a5-f7848b46ac7f
# 93df7064-424e-4221-b8e7-6411839efa29
# 8092a09b-dbbb-4197-9389-652f13e378f4
# 1c8008e8-68de-4e5e-92a2-1735ed25b7e9
# e8e209c5-e891-4468-9e8f-5c758c119f8a
# a3a3f3c3-952d-4725-bd9d-70a98bf46179
# 5cdd388a-cc79-4b4c-a7b2-601740be855a"""
#     raw_list = raw_list.split("\n")


    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    # attrs = ["PseudoColor"]
    # download_raw(table, raw_list1, attrs, "/Users/ziweishi/Desktop/WASP_Mask/")

    attrs = ["Mask", "PseudoColor"]
    download_raw(table, raw_list, attrs, "/Users/ziweishi/Desktop/WASP_Mask/")








