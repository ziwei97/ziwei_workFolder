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

    attrs=["PseudoColor"]

    cor = """9d34e35b-ed2c-400f-b18e-3612be959cf0
24e932b6-c577-452f-aeb6-68cf6cda782e
12dfa884-ce66-437f-b5cb-93981e180277
6766ee4a-1ed9-4112-8698-4aef5fe73837
781c98ec-98b5-48de-a542-68c0d73d45fa
d8efacb9-6a23-48c6-bf65-ad47beaa3322
8b114edc-c4a2-4ab6-9ab0-c2aa05258b92
8abe3dfe-4d43-42f3-944b-34669667ab26
ec55138e-2ad7-4cb6-a087-a7b577201c9b
4d94ddea-72d4-422b-886e-fa8d922a3aa1
88754652-8d9f-4e81-9701-9cdeb472fe2b"""

    path = "/Users/ziweishi/Documents/check/"

    raw_list = cor.split("\n")
    table_name = 'BURN_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    download_raw(table,raw_list,attrs,path)






















