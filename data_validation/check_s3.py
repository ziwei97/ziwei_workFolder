import os
import pandas as pd

# aws s3 ls s3://spectralmd-datashare/DataScience/MSI_Generation_Phase_III_2023-03-14/ --recursive | cat >> /Users/ziweishi/Desktop/s3_list.txt



path = "/Users/ziweishi/Desktop/s3_list.xlsx"
df = pd.read_excel(path,sheet_name="file")
list = pd.read_excel(path,sheet_name="subjectid")
guid=list["list_id"].to_list()


raw = []
assess =[]
mask = []
tattoo = []
p=1
for i in guid:
    subset = df[df["guid"]==i]
    file_list = subset["file"].to_list()
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


    mask.append(mas_num)
    assess.append(ass_num)
    raw.append(raw_num)
    print(p)
    p+=1

final = zip(guid,mask,assess,raw)


data = pd.DataFrame(final,columns=["guid","mask_num","assess_num","raw_num"])
data.to_excel("/Users/ziweishi/Desktop/msi_s3_checking.xlsx")