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

patient_list = ["207-009","208-099","208-000","208-077"]

test = ["000","99","77","88","."]

p_list = [i for i in patient_list if all(text not in i for text in test)]

print(p_list)



#
# structure=["PseudoColor","Assessing","Mask","Phase","Tags"]
# type_list = {i:[] for i in structure}
#
# print(type_list)