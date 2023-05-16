import boto3
import os

import numpy as np
import pandas as pd
import random
import pathlib

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
    os.makedirs(fold)
    for i in raw_list:
        print(index)
        name = get_attribute(table,i,"Bucket")
        folder = os.path.join(fold, i)
        os.makedirs(folder)
        for j in attrs:
            try:
                if j=="PseudoColor":
                    s = "PseudoColor/PseudoColor_" + str(i) + ".tif"
                    file_name = "PseudoColor_" + str(i) + ".tif"
                    file_path = os.path.join(folder, file_name)
                    s3.Bucket(name).download_file(s, str(file_path))
                else:
                    attr = get_attribute(table, i, j)
                    for s in attr:
                        file_name = s.split('/')[-1]
                        file_path = os.path.join(folder, file_name)
                        s3.Bucket(name).download_file(str(s), str(file_path))
            except:
                error_list.append(i)
                print(i)
        index+=1



# raw_list=["58605b44-fdeb-41b9-83b6-56970d13365e"]
# attrs=["Raw","FinalTruth","Mask"]

# table_name = 'DFU_Master_ImageCollections'
# table = dynamodb.Table(table_name)
# download_raw(table,raw_list,attrs,"/Users/ziweishi/Documents/demo1")



def replace_all(text,reo):
    for i in reo:
        if i in text:
            text.replace("i","")
    return text