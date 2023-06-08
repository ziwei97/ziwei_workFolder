import os
import pandas as pd
import numpy as np
import matplotlib.image as image
from PIL import Image
import cv2
import boto3
import download_whole_dynamodb_table


# sql_path = "avhvjdlnjgshg"
#
# print(sql_path[-3:])

# df = pd.read_excel("/Users/ziweishi/Documents/database/DFU_Master_ImageCollections.xlsx")
# list1 = df["Raw"].to_list()
#
# a = list1[0].replace(" ","")
# a = a.strip("{}").split(",")
# b= [i.replace("'","") for i in a]
# c = [i.replace("Raw/Raw_","") for i in b]
# print(c)


# db = download_whole_dynamodb_table.download_table("DFU_Master_ImageCollections")
# db_sub = db[db["ImgCollGUID"] == "00"]
#
# db_raw = db_sub["Raw"].iloc[0]
# print(db_raw)










# s3 = boto3.resource('s3')
# dynamodb = boto3.resource('dynamodb')







#
# table_name = 'BURN_Master_ImageCollections'
# table = dynamodb.Table(table_name)


#
# file_path = "/Users/ziweishi/Downloads/Mask_00075e7c-fa64-47b8-8364-e0690bd33d3e.png"
# img = cv2.imread(file_path)
#
#
# sp = img.shape
# print(sp)

# df = pd.read_excel("/Users/ziweishi/Desktop/file_check.xlsx",sheet_name="Sheet2")
#
# guid = df["ImgCollGUID"].to_list()
# file = df["file"].to_list()

#
# index = 0
#
#
# size=[]
# for i in guid:
#     s3_path = "DataScience/ePOC_All_Data_Request_2023-05-04/"
#     file_s3 = s3_path+i+"/"+file[index]
#     local_path = "/Users/ziweishi/Desktop/epoc_mask/"+i
#     if os.path.isdir(local_path) == False:
#         os.mkdir(local_path)
#     local_file = os.path.join(local_path,file[index])
#     s3.Bucket("spectralmd-datashare").download_file(file_s3, local_file)
#     index+=1
#     img = cv2.imread(local_file)
#     sp = img.shape
#     size.append(sp)
#     print(index)
#     print(sp)
#
#
# df["Size"] = size
#
# df.to_excel("/Users/ziweishi/Desktop/mask_size.xlsx")
#
#
# key = "DataScience/WAUSI_SV0_0522/205-002/SV_1_Date/"
# s3.Object('spectralmd-datashare', key).delete()


# df = pd.read_excel("/Users/ziweishi/Downloads/WASP_Info.xlsx")
#
# df = df[df["Sequence"]==0]
#
# print(len(df))
#
# df.to_excel("/Users/ziweishi/Downloads/WASP_SV0_0522.xlsx")

# guid=df["ImgCollGUID"].to_list()
# file = df["file"].to_list()
# index=0
#
# for i in guid:
#     prefix = "DataScience/WAUSI_PartI_0516/"
#     key = prefix+i+"/"+file[index]
#     s3.Object('spectralmd-datashare', key).delete()
#     index+=1
#     print(index)


#

#
# list = []
# for i in guid:
#     if i not in list:
#         list.append(i)
#
# study = pd.read_excel("/Users/ziweishi/Desktop/BURN_Master_Study.xlsx")
#
#
# study =study[study["ImgCollGUID"].isin(list)]
#
# study = study[["ImgCollGUID","FileName","S3_Location","UploadDate"]]
#
# study.to_excel("/Users/ziweishi/Desktop/Study.xlsx")
#
#
# index=0
# upload_date=[]
# s3_location = []
# for i in guid:
#     subset = study[study["ImgCollGUID"]==i]
#     name = file[index]
#     sub = subset[subset["FileName"]==name]
#
#     try:
#         date = sub["UploadDate"].iloc[0]
#     except:
#         date = np.nan
#     try:
#         s3_loc = sub["S3_Location"].iloc[0]
#     except:
#         s3_loc = np.nan
#
#     upload_date.append(date)
#     s3_location.append(s3_loc)
#     index+=1
#     print(index)
#
# df["date"] = upload_date
# df["s3_location"] = s3_location

# df = pd.read_excel("/Users/ziweishi/Desktop/epoc_mask.xlsx")
# guid=df["ImgCollGUID"].to_list()
# file = df["file"].to_list()
#
# list = []
# for i in guid:
#     if i not in list:
#         list.append(i)
#
#
# index=0
# num = []
# for i in guid:
#     name =file[index].split("_")
#     if len(name) ==2:
#         num.append(1)
#     else:
#         num.append(0)
#
#     index+=1
#
# df["num"] = num
#
#
# df.to_excel("/Users/ziweishi/Desktop/epoc_mask1.xlsx")



#
# path = "/Users/ziweishi/Desktop/sample.xlsx"
# image=np.array("/Users/ziweishi/Downloads/Mask_00075e7c-fa64-47b8-8364-e0690bd33d3e.png")
# print(image.shape)


# image = img.imread('/content/drive/My Drive/Colab Notebooks/rusty.png')

#
# list = os.listdir(path)
# if ".DS_Store" in list:
#     list.remove(".DS_Store")
#
# print(len(list))
#
# guid=[]
# file=[]
# size=[]
#
# p=1
# for i in list:
#     file_path = os.path.join(path,i)
#     file_list = os.listdir(file_path)
#     if ".DS_Store" in file_list:
#         file_list.remove(".DS_Store")
#     for j in file_list:
#         guid.append(i)
#         file.append(j)
#         img_path=os.path.join(file_path,j)
#         a = os.path.getsize(img_path)
#         size.append(a)
#     print(p)
#     p+=1
# final = zip(guid,file,size)
#
# data = pd.DataFrame(final,columns=["guid","file","size"])
# data.to_excel("/Users/ziweishi/Desktop/training.xlsx")
#
# data = pd.read_excel(path)
#
# s = data[data["ImgCollGUID"]=="ba17227d-c5da-4126-be27-d1e6fe7d90db"]
# name = s["Raw"].iloc[0]


# study = pd.read_excel("/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.xlsx")
#
# sub = study["SubjectID"].to_list()
# phase = study["phase"].to_list()
#
# index=0
#
# info={}
# for i in sub:
#     if i not in info:
#         info[i]=phase[index]
#     index+=1
#
# print(info)
#
#
# data = pd.DataFrame.from_dict(info,orient='index')
# sublist=["106-005","108-001","108-002"]
# data = study[study["SubjectID"].isin(sublist)]
#
# data = data[["ImgCollGUID","Status","Tags","SubjectID","UploadDate"]]
# data.to_excel("/Users/ziweishi/Desktop/sub_info.xlsx")
#
#
# path="/Users/ziweishi/Desktop/file_check.xlsx"
# df=pd.read_excel(path)
#
# subject = df["SubjectID"].to_list()
# phase = df["phase number"].to_list()
#
# list = {}
#
#
# a=0
# for i in subject:
#     if i not in list:
#         list[i]= phase[a]
#     a+=1
#
#
# data = pd.DataFrame.from_dict(list,orient='index')
#
# # data.to_excel("/Users/ziweishi/Desktop/subject_check.xlsx")
# # print(data)
#
#
# a='000'
# list=[]
# for i in a:
#     i = int(i)
#     list.append(i)
# b =tuple(list)
# print(b)
#
# import boto3
#
# # 创建S3客户端
# # 指定存储桶名称
# bucket = 'testziwei97'
#
#
#
# def list_bucket_objects(bucket_name):
#     s3 = boto3.client('s3')
#     response = s3.list_objects_v2(Bucket=bucket_name)
#
#     objects = []
#     for obj in response['Contents']:
#         objects.append(obj['Key'])
#
#     while response['IsTruncated']:
#         response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=response['NextContinuationToken'])
#         for obj in response['Contents']:
#             objects.append(obj['Key'])
#
#     return objects
#
# # 使用示例
#
# all = list_bucket_objects(bucket)
#
#
# b = pd.DataFrame(all,columns=["file"])
# b.to_excel("/Users/ziweishi/Desktop/file.xlsx")


df_train = pd.read_excel("/Users/ziweishi/Documents/DFU_regular_update/20230608/toyin_filtered.xlsx")

df_sub = df_train["SubjectID"].to_list()

df= pd.read_excel("/Users/ziweishi/Desktop/dfu_check.xlsx")

df_validation = df[~df["MedicalNumber"].isin(df_sub)]

df_validation.to_excel("/Users/ziweishi/Desktop/dfu_validation.xlsx")



