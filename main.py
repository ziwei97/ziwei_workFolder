import os
import pandas as pd

path = "/Users/ziweishi/Desktop/sample.xlsx"
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

data = pd.read_excel(path)

s = data[data["ImgCollGUID"]=="ba17227d-c5da-4126-be27-d1e6fe7d90db"]
name = s["Raw"].iloc[0]


