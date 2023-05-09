import pandas as pd
import numpy as np
from datetime import datetime


castor = pd.read_excel("/Users/ziweishi/Documents/DFU_regular_update/20230508_Visit_Data.xlsx")
toyin = pd.read_excel("/Users/ziweishi/Downloads/WAUSI.xlsx")


df_toyin = pd.DataFrame()
df_toyin["SubjectID"]  = toyin["Subject ID"]
df_toyin["SV1"]  = toyin["BSV/SV1"]
column = ["SubjectID"]


def change_format(date):

    i = str(date)
    print(i)
    try:
        if "." in i:
            i = datetime.strptime(i, "%m.%d.%y").strftime("%d-%m-%Y")
        if "/" in i:
            i = datetime.strptime(i, "%m/%d/%y").strftime("%d-%m-%Y")
        if "-" in i:
            i = datetime.strptime(i,"%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
    except:
        i = date
        # print(i)
    return i


for i in range(2,13):
    visit = "SV_"+str(i)+"_Date"
    to_vis = "SV"+str(i)
    column.append(visit)
    date_time_list = []
    for i in toyin[to_vis]:
        if type(i)!=float and str(i) !="NaT":
            i = change_format(i)
            date_time_list.append(i)
        else:
            date_time_list.append(np.nan)
    visit_date = pd.DataFrame(date_time_list)
    df_toyin[visit]= visit_date


sub = toyin["Subject ID"].to_list()
castor = castor[castor["SubjectID"].isin(sub)]
castor = castor[column]


df_toyin.to_excel("/Users/ziweishi/Desktop/toyin_filtered.xlsx")
castor.to_excel("/Users/ziweishi/Desktop/castor_filtered.xlsx")


# check visit num
# count_num  = final.count(axis='columns')