import os
import shutil
import boto3
import pandas as pd
import data_validation.test_copy as ts_copy

s3 = boto3.resource('s3')


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


# path = "/Users/ziweishi/Documents/transfer_regular_check/0_sql_file"
# list = os.listdir(path)
#
# for i in list:
#     p = i.split("_")
#     print(p[0]+" "+p[1])

# path = "/Users/ziweishi/Documents/transfer_regular_check/rsci/temp1/rsci_image_log_out.xlsx"
# df = pd.read_excel(path)
#
# path_ass = "/Users/ziweishi/Documents/DFU_regular_update/Phase3_Algorithm_Mask_comment.xlsx"
# df_ass = pd.read_excel(path_ass)
#
# df1 = df[df["Assessing Issue"].isna()]
#
# guid = df1["ImgCollGUID"].to_list()
# loc = df1["File_Location"].to_list()
#
# index=0
#
# for i in guid:
#     loc_s3 = loc[index]
#     index+=1
#     print(index)
#     loc_source = loc_s3.replace("\\","/")
#     loc_source = loc_source.replace("D:","DataTransfer/WAUSI_Connolly_Hospital_Ireland/CONNOLLY_DFU_SMD2211-004_07_03_23")
#     df_sub = df_ass[df_ass["ImgCollGUID"]==i]
#     file = df_sub["Assessing"].iloc[0]
#     file = file[2:-2]
#     file = (file.split("/"))[-1]
#     file = file.replace(".png",".tif")
#     file = file.replace("Assessing_","")
#     file_source =loc_source+"/"+file
#
#     # print(file_source)
#
#     copy_source={
#         'Bucket':"spectralmd-uk" ,
#         'Key': file_source}
#
#     dest_file = "Assessing_"+i+".png"
#     dest_path = "DataScience/WAUSI_Pseudo_Assesing_0725/Assessing/"+dest_file
#
#     s3.meta.client.copy(copy_source, 'spectralmd-datashare', dest_path)












# df.to_excel("/Users/ziweishi/Documents/compare.xlsx")


path ="/Users/ziweishi/Documents/20230727tra_wausi_info.xlsx"
df = pd.read_excel(path)

df = df[df["Comments"]!="archived"]

df= df.reset_index()

df = df.iloc[:,3:]

df.to_csv("/Users/ziweishi/Documents/phase3_wausi_info.csv")

