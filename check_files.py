import os
import pandas as pd

path = "/Users/ziweishi/Users/ziweishi/Data/phase3_msi"

list = os.listdir(path)
if ".DS_Store" in list:
    list.remove(".DS_Store")

# file=[]
# size=[]
# loc=[]
# type=[]

raw = []
assess =[]
mask = []
p=1
for i in list:

    file_path = os.path.join(path,i)
    file_list = os.listdir(file_path)
    if ".DS_Store" in file_list:
        file_list.remove(".DS_Store")

    mas_num = 0
    raw_num = 0
    ass_num = 0
    for j in file_list:
        if j[0:3] =="Mas":
            mas_num+=1
        if j[0:3] =="Raw":
            raw_num+=1
        if j[0:3] =="Ass":
            ass_num+=1

        img_path=os.path.join(file_path,j)
        a = os.path.getsize(img_path)
        if a < 1024:
            print(img_path)

    mask.append(mas_num)
    assess.append(ass_num)
    raw.append(raw_num)
    print(p)
    p+=1


final = zip(list,mask,assess,raw)


data = pd.DataFrame(final,columns=["guid","mask_num","assess_num","raw_num"])

data.to_excel("/Users/ziweishi/Desktop/msi_local_checking.xlsx")