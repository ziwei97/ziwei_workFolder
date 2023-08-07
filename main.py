import os
import shutil
import boto3
import pandas as pd
import data_validation.test_copy as ts_copy
import util.update_attr as update

s3 = boto3.resource('s3')


# key = "DataScience/WAUSI_SV0_0522/205-002/SV_1_Date/"
# s3.Object('spectralmd-datashare', key).delete()


# 指定存储桶名称和前缀
# bucket_name = 'spectralmd-datashare'
# folder_prefix = 'DataScience/rcsi_fix_0802/PseudoColor/'



# bucket = s3.Bucket(bucket_name)
#
# list = []
# for obj in bucket.objects.filter(Prefix=folder_prefix):
#     path = obj.key
#     guid = path.split("/")
#     guid = guid[-1]
#     guid = guid.replace("PseudoColor_","")
#     guid = guid.replace(".tif","")
#     update.update_guid(guid, "phase", 4)
#
#     print(guid)




path = "/Users/ziweishi/Documents/DFU_regular_update/20230807/20230807_Guid_list.xlsx"

df = pd.read_excel(path)

df = df[df["phase"]=="4"]

print(len(df))

df.to_csv("/Users/ziweishi/Desktop/Phase4_All_GUID_Info.csv")



#
# structure=["PseudoColor","Assessing","Mask","Phase","Tags"]
# type_list = {i:[] for i in structure}
#
# print(type_list)