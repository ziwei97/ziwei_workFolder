import os
import pandas as pd
import numpy as np
import matplotlib.image as image
from PIL import Image
import cv2
import boto3
import download_whole_dynamodb_table
import shutil
from datetime import datetime, timedelta

# key = "DataScience/WAUSI_SV0_0522/205-002/SV_1_Date/"
# s3.Object('spectralmd-datashare', key).delete()

#
# guid="""129404cd-b904-4160-85e1-1b071f29a3fc
# 8eee846a-4f03-4ef8-ac34-80bdaf2bc93b
# a65aa2c1-b65a-4eb0-8c12-97c2539f29b6
# 4f9d7034-d81c-428d-8aef-6f633d621c77
# 49405c7a-c862-4fa9-beae-7a0158268c6f
# 0e546fad-f726-4cb1-9003-57b8594830aa
# c17af431-6fc2-4cc4-a772-697d243e75a0
# 80785b2f-bfa2-400f-8e3a-5e541e12d50d
# da057a5e-303e-40ae-83a0-cab1e37f6233
# 2d0e1c2f-b6bf-47ab-95ce-3dff6ab115f5
# 61e62f1c-9b7e-442a-bc8f-0bc35c326787
# f877a769-a601-4e4a-a949-4ccadd4a6d37
# 0c748427-bef6-43e0-9ec6-1af74e07d2c0
# d1ad8ada-a7dc-48c8-964e-633d623d1186
# 8c5f7d90-84b9-41a1-aac9-981d9f12931a"""
#
# guid = guid.split("\n")
#
#
# def move_file(path,target,guid):
#     list1 = os.listdir(path)
#     index = 0
#     list1.remove(".DS_Store")
#     for i in list1:
#         id = guid[index]
#         if "." not in i:
#             guid_path = os.path.join(path, i)
#             target_path = os.path.join(target, id)
#             os.mkdir(target_path)
#             file_list = os.listdir(guid_path)
#             for j in file_list:
#                 if j == "PseudoColor.tif":
#                     pseduo = os.path.join(guid_path, j)
#                     name = "PseudoColor_" + id + ".tif"
#                     t_pseudo = os.path.join(target_path, name)
#                     shutil.copy(pseduo, t_pseudo)
#                 if "Assessing" in j:
#                     ass = os.path.join(guid_path, j)
#                     ass_name = "Assessing_" + id + ".png"
#                     t_ass = os.path.join(target_path, ass_name)
#                     shutil.copy(ass, t_ass)
#         index += 1
#
#
#
# file_names = ["03_01_2023","04_27_2023","06_08_2023","01_01_2022","09_01_2023","10_01_2023"]
#
# max_time= datetime(2020, 1, 1)
# for i in file_names:
#     if "full" in i:
#         max_time = i
#     else:
#         time = i.split("_")
#         year = time[-1]
#         date = time[-2]
#         month = time[-3]
#         date_time = month + "/" + date + "/" + year
#         real_time = datetime.strptime(date_time, '%m/%d/%Y')
#         if real_time > max_time:
#             max_time = real_time
#         else:
#             max_time = max_time
#
#
# print(max_time)

#
# local_site = ["nynw","ocer","whfa","youngst","lvrpool","memdfu","hilloh","grovoh","mentoh","encinogho","lahdfu"]
# s3_site=["rsci"]
#
# total_site=local_site+s3_site
#
#
#
# site_list={}
# for i in total_site:
#     site_list[i]={}
#     if i in local_site:
#         site_list[i]["type"] = "local"
#     else:
#         site_list[i]["type"] = "s3"
#
#
# print(site_list["youngst"]["type"])


path = "/Users/ziweishi/Documents/transfer_regular_check/sql_file/"
if os.path.isdir(path) == True:
    shutil.rmtree(path)

os.mkdir(path)