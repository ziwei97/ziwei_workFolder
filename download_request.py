import boto3
import os

import numpy as np
import pandas as pd
import random
import pathlib

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

table_name = 'BURN_Master_ImageCollections'
table = dynamodb.Table(table_name)

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

#
# df = pd.read_excel("/Users/ziweishi/Desktop/All_Phase_BURN.xlsx",sheet_name="exclude_fromLeo")
# guid = df["ImgCollGUID"].to_list()
# tags = []
# status = []
# final = []
# mask = []
# a=0
# for i in guid:
#     tag = get_attribute(table,i,"Status")
#
#     # sta = get_attribute(table,i,"Status")
#     # fi = get_attribute(table,i,"FinalTruth")
#     # ma = get_attribute(table,i,"Mask")
#     # final.append(fi)
#     # mask.append(ma)
#     # tags.append(tag)
#     # status.append(sta)
#     print(tag)
#     # a+=1
#     # print(a)


# df["Status"] = status
# df["FinalTruth"] = final
# df["Mask"]= mask
# df["Tags"] = tags
#
# df.to_excel("/Users/ziweishi/Desktop/no_mask1.xlsx")


#
# status=[]
# pseudo = []
# assessing = []
# mask = []
#
# a=0
# for i in guid:
#     sta = get_attribute(table,i,"Status")
#     pseu = get_attribute(table,i,"PseudoColor")
#     ass = get_attribute(table,i,"Assessing")
#     ma = get_attribute(table,i,"Mask")
#
#     status.append(sta)
#     pseudo.append(pseu)
#     assessing.append(ass)
#     mask.append(ma)
#     print(a)
#     a+=1
#
# df["Status"] = status
# df["PseudoColor"] = pseudo
# df["Assessing"] = assessing
# df["Mask"] = mask
#
# df.to_excel("/Users/ziweishi/Desktop/num_check1.xlsx")




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



raw_list=["ba17227d-c5da-4126-be27-d1e6fe7d90db"]
attrs=["PseudoColor","FinalTruth","Mask"]
# attrs=["Assessing","Raw","PseudoColor","FinalTruth","Mask"]
download_raw(table,raw_list,attrs,"/Users/ziweishi/Documents/demo")



def replace_all(text,reo):
    for i in reo:
        if i in text:
            text.replace("i","")
    return text