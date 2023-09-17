import os
import shutil
import boto3
import numpy as np
import pandas as pd
import data_validation.test_copy as ts_copy
import util.download_request as download_request
import util.download_whole_dynamodb_table as download_table

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


# key = "DataScience/WAUSI_SV0_0522/205-002/SV_1_Date/"
# s3.Object('spectralmd-datashare', key).delete()


# 指定存储桶名称和前缀
# bucket_name = 'spectralmd-datashare'
# folder_prefix = 'DataScience/rcsi_fix_0802/PseudoColor/'

# patient_list = ["207-009","208-099","208-000","208-077"]
#
# test = ["000","99","77","88","."]
#
# p_list = [i for i in patient_list if all(text not in i for text in test)]
#
# print(p_list)



#
# structure=["PseudoColor","Assessing","Mask","Phase","Tags"]
# type_list = {i:[] for i in structure}
#
# print(type_list)
table_name = 'BURN_Master_ImageCollections'
table = dynamodb.Table(table_name)

df = pd.read_excel("/Users/ziweishi/Downloads/bts_all_phase_info.xlsx")



db = pd.read_excel("/Users/ziweishi/Documents/ziwei_project/Documents/Database/BURN_Master_ImageCollections.xlsx")



guid = df["ImgCollGUID"].to_list()
subject = df["SubjectID"].to_list()
wound_list = df["Wound"].to_list()
id_list = df["ImageCollectionID"].to_list()
capture_time = df["CaptureDate"].to_list()

ImageCollTime = []
jsonfile = []
index = 0

insert_position1 = df.columns.get_loc('CaptureDate') - 1
insert_position2 = df.columns.get_loc('CaptureDate')
for i in guid:
    # b = download_request.get_attribute(table,i,"Bucket")
    b = db[db["ImgCollGUID"]==i]

    bucket = b["Bucket"].iloc[0]
    sub = subject[index]
    id = id_list[index]
    wound = wound_list[index]
    json = sub+"_"+str(wound)+"_"+bucket+"_SS_"+str(id)+".json"
    jsonfile.append(json)

    cap = str(capture_time[index]).split(" ")
    time = cap[1].replace(":",".")
    cap_time = cap[0]+"_"+time+".000"
    ImageCollTime.append(cap_time)
    index+=1
    print(index)

df.insert(insert_position1,"jsonFile",jsonfile)
df.insert(insert_position2,"ImageCollTime",ImageCollTime)
df.to_csv("/Users/ziweishi/Downloads/bts_all_phase_info.csv")