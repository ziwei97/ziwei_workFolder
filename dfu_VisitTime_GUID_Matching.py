import os.path

import pandas as pd
from datetime import datetime, timedelta
import download_whole_dynamodb_table
import numpy as np



def parse_date(x):
    try:
        stamp = int(x) - 2209031999999999700
        eval = str(pd.to_datetime(stamp).strftime('%d-%m-%Y'))
    except:
        eval = np.nan
    return eval

def fuzzy_date_match(date1, date2, day_range, date_format='%d-%m-%Y'):
    if not date1 or not date2:
        return '-'
    if isinstance(date1, float) or isinstance(date2, float):
        return '-'
    if date1 == "##USER_MISSING_96##" or date2 == "##USER_MISSING_96##" or date1 == "##USER_MISSING_99##" or date2 == "##USER_MISSING_99##":
        return '-'
    delta = timedelta(days=day_range)
    date1 = datetime.strptime(date1, date_format)
    date2 = datetime.strptime(date2, date_format)
    range_start = date1 - delta
    range_end = date1 + delta
    # print(f'Is {date2} in between {range_start} and {range_end}')
    if range_start <= date2 <= range_end:
        return True
    return False


#
# def change_format(date):
#     i = str(date)
#     if "." in i:
#         i = datetime.strptime(i, "%m.%d.%y").strftime("%d-%m-%Y")
#     if "/" in i:
#         i = datetime.strptime(i, "%m/%d/%y").strftime("%d-%m-%Y")
#     if "-" in i:
#         try:
#             i = datetime.strptime(i, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
#         except:
#             i = datetime.strptime(i, "%d-%m-%Y").strftime("%d-%m-%Y")
#     return i
#
#
# def clean_toyin():
#     toyin = pd.read_excel("/Users/ziweishi/Downloads/WAUSI Completion Tracker Data Analysis 4-14-2023.xlsx",
#                           sheet_name="Sheet2")
#     df_toyin = pd.DataFrame()
#     df_toyin["SubjectID"] = toyin["Subject ID"]
#     column = ["SubjectID"]
#
#     for i in range(1, 13):
#         visit = "SV_" + str(i) + "_Date"
#         to_vis = "SV" + str(i)
#         column.append(visit)
#         date_time_list = []
#         for i in toyin[to_vis]:
#             if type(i) != float:
#                 i = change_format(i)
#                 date_time_list.append(i)
#             else:
#                 date_time_list.append(i)
#         visit_date = pd.DataFrame(date_time_list)
#         df_toyin[visit] = visit_date
#     return df_toyin


def clean_dfu_db():
    guid = download_whole_dynamodb_table.download_table('DFU_Master_ImageCollections')
    guid = guid[['SubjectID', 'ImgCollGUID', 'CreateTimeStamp', 'Status']]
    guid = guid[guid["Status"] == "acquired"]
    guid = guid[guid["CreateTimeStamp"].notna()]
    guid["VisitDate"] = guid[["CreateTimeStamp"]].apply(lambda x: parse_date((x['CreateTimeStamp'])), axis=1)

    sub = guid[['SubjectID', 'ImgCollGUID', 'VisitDate']]

    return sub



def time_table_transfer(update_date):
    og_path = "/Users/ziweishi/Documents/DFU_regular_update/"
    path = os.path.join(og_path,update_date)
    if os.path.isdir(path)==False:
        os.mkdir(path)

    vt = pd.read_excel("/Users/ziweishi/Desktop/toyin_filtered.xlsx")
    sub = clean_dfu_db()
    vt_sub = vt["SubjectID"].to_list()
    list_b = []
    time_order = []
    visit_b = []
    time_match = []

    #timetable frame
    for i in vt_sub:
        for j in range(1, 13):
            time_type = "SV_" + str(j) + "_Date"
            vt_subset = vt[vt["SubjectID"] == i]
            time_v = vt_subset[time_type].iloc[0]
            list_b.append(i)
            time_order.append(time_type)
            visit_b.append(time_v)
        list_b.append(i)
        time_order.append("none_match")
        visit_b.append("none_match")


    data = zip(list_b, time_order, visit_b)
    time_table = pd.DataFrame(data=data, columns=["SubjectID", "VisitTime", "Castor_Date"])

    #match device and toyin list timetable
    for j in vt_sub:
        sub_set = sub[sub["SubjectID"] == j]
        time_set = time_table[time_table["SubjectID"] == j]
        sub_date = sub_set["VisitDate"].to_list()
        time_date = time_set["Castor_Date"].to_list()
        matched_date = []
        date_none = []
        for x in time_date:
            date_list = []
            if "none" not in str(x):
                for y in sub_date:
                    if fuzzy_date_match(x, y, 2, date_format='%d-%m-%Y') == True:
                        if y not in date_list:
                            date_list.append(y)
                            matched_date.append(y)
                time_match.append(date_list)
            if "none" in str(x):
                for p in sub_date:
                    if p not in matched_date:
                        date_none.append(p)
                time_match.append(date_none)
    data1 = zip(list_b, time_order, visit_b,time_match)
    matched_timetable = pd.DataFrame(data=data1, columns=["SubjectID", "VisitTime", "Castor_Date","Match_Date"])

    #group guid table by sub+capture date(VisitDate)
    sub_id = sub["SubjectID"].to_list()
    guid_list = sub["ImgCollGUID"].to_list()
    sub_visit = sub["VisitDate"].to_list()
    sub_cri = []
    for i in range(len(sub_id)):
        date = sub_visit[i]
        cri = str(sub_id[i]) + " " + str(sub_visit[i])
        sub_cri.append(cri)
    data = zip(sub_cri, guid_list)
    df = pd.DataFrame(data=data, columns=["sub_time", "guid"])
    df1 = df.groupby('sub_time')['guid'].apply(list).reset_index(name='new')

    # map guid with sub+capture date check key to toyin list
    list_sub = matched_timetable["SubjectID"].to_list()
    list_time1 = matched_timetable["Match_Date"].to_list()
    list_time=[]
    for i in list_time1:
        if len(i)>0:
            i = str(i)
            i = i.replace("'", "")
            i = i.replace("[", "")
            i = i.replace("]", "")
            i = i.split(",")
        list_time.append(i)
    list_com = []

    for i in range(len(list_sub)):
        x = list_sub[i]
        list_pic = []
        for j in list_time[i]:
            p = str(x) + " " + str(j)
            list_pic.append(p)
        list_com.append(list_pic)

    list_guid = []
    subjectid_list=[]
    visitime_list = []
    guid_final_list=[]
    capture_date = []
    castor_date=[]
    for i in range(len(list_com)):
        list_guid_pic = []
        subjectid = list_b[i]
        visit_time = time_order[i]
        for j in list_com[i]:
            try:
                sub_set = df1[df1["sub_time"] == j]
                value = sub_set["new"].iloc[0]
            except:
                value = []
            if len(value) > 0:
                for p in value:
                    list_guid_pic.append(p)
        list_guid.append(list_guid_pic)

        if "none" not in visit_time:
            for h in list_guid_pic:
                subjectid_list.append(subjectid)
                visitime_list.append(visit_time)
                guid_final_list.append(h)
                cap_date_set = sub[sub["ImgCollGUID"]==h]
                cap_date = cap_date_set["VisitDate"].iloc[0]
                capture_date.append(cap_date)
                castor_date.append(visit_b[i])


    # output guid list
    list_file_name = str(update_date) + "_Guid_list.xlsx"
    list_final_path = os.path.join(path, list_file_name)
    final_guid = zip(subjectid_list,visitime_list,castor_date,capture_date,guid_final_list)
    final_guid_df = pd.DataFrame(final_guid,columns=["SubjectID", "VisitTime","Castor_Date", "Capture_Date", "ImgCollGUID"])
    final_guid_df.to_excel(list_final_path)
    print("total matched guid num: " +str(len(guid_final_list)))

    # output match situation frame
    match_file_name = str(update_date) + "_matched_Guid.xlsx"
    match_final_path = os.path.join(path, match_file_name)
    data_guid = zip(list_b, time_order, visit_b, time_match, list_guid)
    df_final = pd.DataFrame(data=data_guid,columns=["SubjectID", "VisitTime", "Castor_Date", "Match_Device_Date", "ImgCollGUID"])
    df_final.to_excel(match_final_path)

    return df_final


time_table_transfer("20230508")