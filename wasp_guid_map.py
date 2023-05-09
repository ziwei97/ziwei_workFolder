import pandas as pd
import numpy as np
import datetime




def parse_date(x):
    stamp = int(x) - 2209031999999999700
    print(stamp)
    eval = str(pd.to_datetime(stamp).strftime("%d-%m-%Y, %H:%M:%S"))
    return eval



df = pd.read_excel("/Users/ziweishi/Desktop/DataSummary.xlsx")
date = df["date_dd-mm-yyyy"]
time = df["time_hh:mm:ss"]

date1 = []
for i in date:
    p = i.date()

    eval = p.strftime("%d-%m-20%y")
    date1.append(str(eval))

time1 = []
for j in time:

    eval = j.replace(".",":")
    time1.append(eval)


df["date_dd-mm-yyyy"]=date1
df["time_hh:mm:ss"]=time1

df.to_excel("/Users/ziweishi/Desktop/DataSummary1.xlsx")



# for i in guid_list:
#     df1=df[df["ImgCollGUID"]==i]
#     create = df1["CreateTimeStamp"].iloc[0]
#     time_pair = parse_date(create)
#     mid_time = parse_mid_date(create)
#     # day = time_pair.split(",")
#
#     date_time.append(time_pair)
#     mid_time_list.append(mid_time)
#     print(index)
#     index+=1

#
# dfu["UTC_date_time"] = date_time
#
# dfu["Mid_date_time"]=mid_time_list
#
# # data = zip(guid_list,subjectID_list,wound_list,imgID_list,site_list,ssp_json,status_list,visit_date_list)
#
# # final = pd.DataFrame(data,columns=["ImgCollGUID","SubjectID","Wound","ImageCollectionID","Site","jsonFile","Status","VisitDate"])
# #
# dfu.to_csv("/Users/ziweishi/Desktop/WAUSI_Info.csv")