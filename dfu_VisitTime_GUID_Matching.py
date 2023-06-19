import os.path

import pandas as pd
from datetime import datetime, timedelta
import download_whole_dynamodb_table
import numpy as np
import toyin_castor_check



def parse_date(x):
    try:
        stamp = int(x) - 2209031999999999700 - 6*60*60*1000000000
        eval = str(pd.to_datetime(stamp).strftime('%d-%m-%Y'))
    except:
        eval = np.nan
    return eval

def parse_time(x):
    try:
        stamp = int(x) - 2209031999999999700- 6*60*60*1000000000
        eval = str(pd.to_datetime(stamp).strftime('%d-%m-%Y %H:%M:%S'))
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

def clean_dfu_db(check_date):
    guid = download_whole_dynamodb_table.download_table('DFU_Master_ImageCollections')
    guid = guid[guid["StudyName"]=="DFU_SSP"]
    guid = guid[['SubjectID', 'ImgCollGUID', 'CreateTimeStamp', 'Status','Tags','Mask','PseudoColor',"Assessing"]]
    guid = guid[guid["Status"] == "acquired"]
    guid = guid[guid["CreateTimeStamp"].notna()]
    guid["VisitDate"] = guid[["CreateTimeStamp"]].apply(lambda x: parse_date((x['CreateTimeStamp'])), axis=1)
    guid["UTC_Time"] =  guid[["CreateTimeStamp"]].apply(lambda x: parse_time((x['CreateTimeStamp'])), axis=1)

    sub = guid[['SubjectID', 'ImgCollGUID', 'VisitDate',"UTC_Time","Tags","Mask","PseudoColor","Assessing"]]
    list = sub["ImgCollGUID"].to_list()
    time = sub["UTC_Time"].to_list()
    tag = sub["Tags"].to_list()
    mask = sub["Mask"].to_list()
    pseudo = sub["PseudoColor"].to_list()
    assessing=sub["Assessing"].to_list()
    guid_time = {}
    tags={}
    masks={}
    pseudos={}
    assess={}
    index=0
    for i in list:
        guid_time[i]=time[index]
        tags[i]=tag[index]
        masks[i]=mask[index]
        pseudos[i]=pseudo[index]
        assess[i]=assessing[index]
        index+=1

    path ="/Users/ziweishi/Documents/DFU_regular_update/"+check_date+"/database"+"_"+check_date+".xlsx"
    sub.to_excel(path)
    print("total device collection num is: " + str(len(sub)))


    return sub,guid_time,tags,masks,pseudos,assess



def time_table_transfer(update_date):
    og_path = "/Users/ziweishi/Documents/DFU_regular_update/"
    path = os.path.join(og_path,update_date)
    if os.path.isdir(path)==False:
        os.mkdir(path)

    #step 1 return subject list
    vt1 = toyin_castor_check.clean_track(update_date)
    vt = vt1[0]
    db_info = clean_dfu_db(update_date)
    sub = db_info[0]
    vt_sub = vt["SubjectID"].to_list()
    list_b = []
    time_order = []
    visit_b = []
    time_match = []


    #step 2 append castor date to subjects
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


    #step 3 append device date to subject+castor date
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
                    if fuzzy_date_match(x, y, 1, date_format='%d-%m-%Y') == True:
                        if y not in date_list:
                            date_list.append(y)
                            matched_date.append(y)
                time_match.append(date_list)
            if "none" in str(x):
                for p in sub_date:
                    if p not in matched_date:
                        if p not in date_none:
                            date_none.append(p)
                time_match.append(date_none)
    data1 = zip(list_b, time_order, visit_b,time_match)
    matched_timetable = pd.DataFrame(data=data1, columns=["SubjectID", "VisitTime", "Castor_Date","Match_Date"])
    matched_timetable.to_excel("/Users/ziweishi/Downloads/check.xlsx")


    #step 4 append guid to sub+castor+match device with key sub+device date
    sub_id = sub["SubjectID"].to_list()
    guid_list = sub["ImgCollGUID"].to_list()
    sub_visit = sub["VisitDate"].to_list()
    sub_cri = []
    for i in range(len(sub_id)):
        cri = str(sub_id[i]) + " " + str(sub_visit[i])
        sub_cri.append(cri)
    data = zip(sub_cri, guid_list)
    df = pd.DataFrame(data=data, columns=["sub_time", "guid"])
    df1 = df.groupby('sub_time')['guid'].apply(list).reset_index(name='new')

    list_sub = matched_timetable["SubjectID"].to_list()
    list_time1 = matched_timetable["Match_Date"].to_list()
    list_time=[]
    for i in list_time1:
        if len(i)>0:
            i = str(i)
            # i = i.strip('][').split(',')
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

    num_list =[]
    total_none_match=0

    for i in range(len(list_com)):
        list_guid_pic = []
        subjectid = list_b[i]
        visit_time = time_order[i]
        num=0
        for j in list_com[i]:
            try:
                sub_set = df1[df1["sub_time"] == j]
                value = sub_set["new"].iloc[0]
            except:
                value = []
            if len(value) > 0:
                for p in value:
                    num+=1
                    list_guid_pic.append(p) #add guid to sub+time key pair
        list_guid.append(list_guid_pic)
        num_list.append(num)
        if "none" in visit_time:
            total_none_match+=num

        #add guid to output matched guid file
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
    time_list=[]
    time_info=db_info[1]
    tag_info=db_info[2]
    mask_info=db_info[3]
    pseudo_info = db_info[4]
    assess_info = db_info[5]
    list_file_name = str(update_date) + "_Guid_list.xlsx"
    list_final_path = os.path.join(path, list_file_name)
    final_guid = zip(subjectid_list,visitime_list,castor_date,capture_date,guid_final_list)

    issue = vt1[1]
    status = vt1[2]
    index=0
    collection_type=[]
    tags_add=[]
    mask_db=[]
    pseudo_db=[]
    assess_db=[]
    status_final=[]
    out_num=0
    for i in guid_final_list:
        subject = subjectid_list[index]
        sta = status[subject]
        status_final.append(sta)
        castor_time=castor_date[index]
        if subject in issue:
            issue_list = issue[subject]
            if castor_time in issue_list:
                collection_type.append("out of 12 weeks")
                out_num += 1
            else:
                collection_type.append(np.nan)
        else:
            collection_type.append(np.nan)

        time_utc = time_info[i]
        time_list.append(time_utc)
        tag_id = tag_info[i]
        tags_add.append(tag_id)
        mask_db.append(mask_info[i])
        pseudo_db.append(pseudo_info[i])
        assess_db.append(assess_info[i])

        index+=1


    final_guid_df = pd.DataFrame(final_guid,columns=["SubjectID", "VisitTime","Castor_Date", "Capture_Date", "ImgCollGUID"])
    final_guid_df["Status"] = status_final
    final_guid_df["CST_Time"]=time_list
    final_guid_df["12 Weeks Check"]= collection_type
    final_guid_df["Tags"]=tags_add
    final_guid_df["Mask"]=mask_db
    final_guid_df["PseudoColor"]=pseudo_db
    final_guid_df["Assessing"] = assess_db
    final_guid_df.to_excel(list_final_path)
    print("total matched guid num: " +str(len(guid_final_list)))
    print("total non-matched guid num: " + str(total_none_match))
    print("total out off 12 weeks guid num: " + str(out_num))



    # output match situation frame
    match_file_name = str(update_date) + "_matched_Guid.xlsx"
    match_final_path = os.path.join(path, match_file_name)
    data_guid = zip(list_b, time_order, visit_b, time_match, num_list,list_guid)
    df_final = pd.DataFrame(data=data_guid,columns=["SubjectID", "VisitTime", "Castor_Date", "Match_Device_Date","Num_GUID", "ImgCollGUID"])
    df_final.to_excel(match_final_path)

    return df_final


if __name__ == "__main__":
    time_table_transfer("20230619")

