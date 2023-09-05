import os
import shutil
import boto3
import numpy as np
import pandas as pd
import data_validation.test_copy as ts_copy
import util.update_attr as update

s3 = boto3.resource('s3')


# key = "DataScience/WAUSI_SV0_0522/205-002/SV_1_Date/"
# s3.Object('spectralmd-datashare', key).delete()


# 指定存储桶名称和前缀
# bucket_name = 'spectralmd-datashare'
# folder_prefix = 'DataScience/rcsi_fix_0802/PseudoColor/'

# patient_list = ["207-009","208-099","208-000","208-077"]
#
# test = ["000","99","77","88","."]
#
# p_list = [i for i in patient_list if all(text not in i for text in test)]
#
# print(p_list)



#
# structure=["PseudoColor","Assessing","Mask","Phase","Tags"]
# type_list = {i:[] for i in structure}
#
# print(type_list)

df = pd.read_excel("/Users/ziweishi/Documents/DFU_regular_update/20230830training/20230830training_Guid_list.xlsx")
sub_list = df["SubjectID"].to_list()
vis_list = df["VisitTime"].to_list()

draw_df = df[df["phase"].notna()]
draw_df = draw_df[draw_df["phase"]!="archived"]
draw_sub = draw_df["SubjectID"].to_list()
draw = {}
for i in draw_sub:
    if i not in draw:
        draw[i] =1
    else:
        draw[i]+=1

archive_df = df[df["phase"]=="archived"]
archive_sub = archive_df["SubjectID"].to_list()
archive = {}
for i in archive_sub:
    if i not in archive:
        archive[i] =1
    else:
        archive[i]+=1


info ={}
num = {}

index = 0
for i in sub_list:
    if i not in num:
        num[i] =1
    else:
        num[i]+=1

    vis = vis_list[index]
    if i not in info:
        info[i] = []
        info[i].append(vis)
    else:
        if vis not in info[i]:
            info[i].append(vis)
        else:
            info[i] = info[i]
    index+=1


subject = info.keys()

time = ["Match","Draw","Archive"]

for i in range(1,13):
    p = "SV_" +str(i)+'_Date'
    time.append(p)


time = time.append("Visit_Total")

df_info = pd.DataFrame(columns=time)

for i in subject:
    vis_info = info[i]
    vis_total = len(info[i])
    for j in vis_info:
        df_info.loc[i,j] = 1

    df_info.loc[i,"Visit_Total"] = vis_total
    try:
        df_info.loc[i, "Match"] = num[i]
    except:
        df_info.loc[i, "Match"] = np.NAN

    try:
        df_info.loc[i,"Drawn"] = draw[i]
    except:
        df_info.loc[i,"Drawn"] = 0

    try:
        df_info.loc[i,"Archive"] = archive[i]
    except:
        df_info.loc[i,"Archive"] = 0



df_info.to_excel("/Users/ziweishi/Documents/vis.xlsx")






