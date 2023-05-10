import os
import pandas as pd
import numpy as np
import matplotlib.image as image
from PIL import Image
import cv2
import boto3

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

table_name = 'BURN_Master_ImageCollections'
table = dynamodb.Table(table_name)


#
# file_path = "/Users/ziweishi/Downloads/Mask_00075e7c-fa64-47b8-8364-e0690bd33d3e.png"
# img = cv2.imread(file_path)
#
#
# sp = img.shape
# print(sp)

# df = pd.read_excel("/Users/ziweishi/Desktop/epoc_all_mask_size.xlsx",sheet_name="Sheet2")
#
# guid = df["ImgCollGUID"].to_list()
# file = df["file"].to_list()


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

# df.to_excel("/Users/ziweishi/Desktop/epoc_all_mask_size.xlsx")

df = pd.read_excel("/Users/ziweishi/Desktop/epoc_all_mask_size.xlsx",sheet_name="Sheet5")

guid=df["ImgCollGUID"].to_list()
file = df["file"].to_list()
index=0

for i in guid:
    prefix = "DataScience/ePOC_All_Data_Request_2023-05-04/"
    key = prefix+i+"/"+file[index]
    s3.Object('spectralmd-datashare', key).delete()
    index+=1
    print(index)

















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


