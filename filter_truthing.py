import pandas as pd
import os

df = pd.read_csv("/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.csv")

data = df[df["Status"]=="acquired"]

print(len(data))
data = data[data["PrimaryDoctorTruth"].isna()]
print(len(data))

data = data[data["SecondaryDoctorTruth"].isna()]
print(len(data))

data = data[data["FinalTruth"].isna()]
print(len(data))

# data = data[data["Tags"].isna()]
# print(len(data))

# data =data[["SubjectID","ImgCollGUID","Site","Wound","Status","Tags"]]
# data.to_csv("/Users/ziweishi/Documents/database/filtered.csv")


df = pd.read_excel("/Users/ziweishi/Downloads/untruthed_collections_20230208.xlsx")

list = df["GUIDs"].to_list()
subject_id = df["SubjectID"].to_list()

guid_list = []
subject_list = []
a=0
for i in list:
    id_list = i.split(",")

    for j in id_list:
        guid = j.replace("'","")
        guid = guid.replace("[","")
        guid = guid.replace("]","")
        guid = guid.replace(" ","")
        guid_list.append(guid)
        subject_list.append(subject_id[a])
    a+=1

final = zip(subject_list,guid_list)

guid_data = pd.DataFrame(data=final,columns=["SubjectID","GUID"])
guid_data.to_csv("/Users/ziweishi/Downloads/corey_guid.csv")

