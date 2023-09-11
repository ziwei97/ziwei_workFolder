import os.path
import pandas as pd
from datetime import datetime, timedelta
from util import download_whole_dynamodb_table
import numpy as np
import toyin_castor_check
import boto3
import util.server_all_output as server_all_output

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

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

def clean_dfu_db(check_date,sub_list):
    db_info = download_whole_dynamodb_table.download_table('DFU_Master_ImageCollections')
    guid =  server_all_output.output_total()
    guid = guid[['MedicalNumber', 'ImgCollGUID', 'CaptureDate',"ImageCollFolderName"]]
    guid['SubjectID']=guid['MedicalNumber']
    guid = guid[['SubjectID', 'ImgCollGUID', 'CaptureDate',"ImageCollFolderName"]]

    guid["VisitDate"] = guid[["CaptureDate"]].apply(lambda x: parse_date((x['CaptureDate'])), axis=1)
    guid["UTC_Time"] =  guid[["CaptureDate"]].apply(lambda x: parse_time((x['CaptureDate'])), axis=1)

    sub = guid[['SubjectID', 'ImgCollGUID', 'VisitDate',"UTC_Time","ImageCollFolderName"]]
    sub_copy = sub.copy()
    sub_copy.loc[sub_copy["SubjectID"].str.contains("206-001"), "SubjectID"] = sub_copy.loc[
        sub_copy["SubjectID"].str.contains("206-001"), "SubjectID"].str.replace("206-001", "206-002")

    sub = sub_copy
    sub = sub[sub["SubjectID"].isin(sub_list)]

    path ="../../Documents/DFU_regular_update/"+check_date+"/database"+"_"+check_date+".xlsx"
    sub.to_excel(path)
    print("total device collection num is: " + str(len(sub)))

    return sub,db_info

def training_time_table_transfer(update_date):
    og_path = "../../DFU_regular_update/"
    path = os.path.join(og_path,update_date)
    if os.path.isdir(path)==False:
        os.mkdir(path)

    #training toyin
    vt1 = toyin_castor_check.clean_training_track(update_date)


    vt = vt1[0]
    issue = vt1[1]
    status = vt1[2]

    vt_sub = vt["SubjectID"].to_list()
    db_info = clean_dfu_db(update_date,vt_sub)
    db_source = db_info[1]

    sub = db_info[0]
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
    df1 = df.groupby('sub_time',group_keys=False)['guid'].apply(list).reset_index(name='new')
    df1.to_excel("/Users/ziweishi/Downloads/check1.xlsx")

    list_sub = matched_timetable["SubjectID"].to_list()
    list_time1 = matched_timetable["Match_Date"].to_list()
    list_time=[]
    for i in list_time1:
        if len(i)>0:
            i = str(i)
            # i = i.strip('][').split(',')
            i = i.replace("'", "")
            i = i.replace(" ", "")
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
    sub_status=[]

    none_match_subject=[]
    none_match_guid=[]
    none_cap_date=[]

    for i in range(len(list_com)):
        subjectid = list_b[i]
        visit_time = time_order[i]
        sta = status[subjectid]
        sub_status.append(sta)
        list_guid_pic = []  # 创建用于存储所有迭代结果的列表

        for j in list_com[i]:
            try:
                sub_set = df1[df1["sub_time"] == j]
                value_list = sub_set["new"].iloc[0]
                # print(len(value_list))
                for r in value_list:
                    list_guid_pic.append(r)
            except:
                list_guid_pic= list_guid_pic


        num = len(list_guid_pic)

        list_guid.append(list_guid_pic)

        num_list.append(num)
        if "none" in visit_time:
            total_none_match+=num
            for u in list_guid_pic:
                none_match_subject.append(subjectid)
                none_match_guid.append(u)
                none_date_set = sub[sub["ImgCollGUID"]==h]
                none_date = none_date_set["VisitDate"].iloc[0]
                none_cap_date.append(none_date)


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
    list_file_name = str(update_date) + "_Guid_list.xlsx"
    list_final_path = os.path.join(path, list_file_name)
    final_guid = zip(subjectid_list,visitime_list,castor_date,capture_date,guid_final_list)

    check_type=["PseudoColor","Assessing","Mask","phase","Tags","Status"]

    source_info = {i: [] for i in check_type}
    server_info = []

    index=0
    collection_type=[]
    status_final=[]
    out_num=0
    for i in guid_final_list:
        sub_source = db_source[db_source["ImgCollGUID"]==i]
        server_source = sub[sub["ImgCollGUID"]==i]
        local_path = server_source["ImageCollFolderName"].iloc[0]
        server_info.append(local_path)
        for s in check_type:
            try:
                value = sub_source[s].iloc[0]
                source_info[s].append(value)
            except:
                source_info[s].append(np.nan)

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
        index+=1



    final_guid_df = pd.DataFrame(final_guid,columns=["SubjectID", "VisitTime","Castor_Date", "Capture_Date", "ImgCollGUID"])
    final_guid_df["Complete_Status"] = status_final
    final_guid_df["12 Weeks Check"]= collection_type
    final_guid_df["ImageCollFolderName"] = server_info

    for y in check_type:
        final_guid_df[y] = source_info[y]
    final_guid_df.to_excel(list_final_path)
    final_guid_df.to_excel("../Documents/dfu_latest_match_training.xlsx")
    print("total matched guid num: " +str(len(guid_final_list)))
    print("total non-matched guid num: " + str(total_none_match))
    print("total out off 12 weeks guid num: " + str(out_num))

    list_download_name = str(update_date) + "_download_list.xlsx"
    list_download_path = os.path.join(path, list_download_name)
    final_download_df = final_guid_df[final_guid_df["phase"].isna()]
    final_download_df.to_excel(list_download_path)
    final_download_df.to_excel("../Documents/download_file/tra_download_list.xlsx")


    final_none_match = zip(none_match_subject,none_match_guid,none_cap_date)
    final_none_df = pd.DataFrame(final_none_match,columns=["SubjectID","ImgCollGUID","VisitTime"])
    list_none_name = str(update_date) + "_none_match_list.xlsx"
    list_none_path = os.path.join(path, list_none_name)
    final_none_df.to_excel(list_none_path)


    # output match situation frame
    match_file_name = str(update_date) + "_matched_Guid.xlsx"
    match_final_path = os.path.join(path, match_file_name)
    data_guid = zip(list_b, sub_status,time_order, visit_b, time_match, num_list,list_guid)
    df_final = pd.DataFrame(data=data_guid,columns=["SubjectID", "Complete_Status","VisitTime", "Castor_Date", "Match_Device_Date","Num_GUID", "ImgCollGUID"])
    df_final.to_excel(match_final_path)
    return df_final

def validation_time_table_transfer(update_date):
    og_path = "/Users/ziweishi/Documents/DFU_regular_update/"
    path = os.path.join(og_path, update_date)
    if os.path.isdir(path) == False:
        os.mkdir(path)

    # validation toyin
    vt1 = toyin_castor_check.clean_validation_track(update_date)

    # #validation toyin
    # vt1 = toyin_castor_check.clean_validation_track(update_date)

    vt = vt1[0]
    issue = vt1[1]
    status = vt1[2]

    vt_sub = vt["SubjectID"].to_list()

    print(len(vt))
    db_info = clean_dfu_db(update_date, vt_sub)
    db_source = db_info[1]

    sub = db_info[0]
    list_b = []
    time_order = []
    visit_b = []
    time_match = []

    # step 2 append castor date to subjects
    # timetable frame
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

    # step 3 append device date to subject+castor date
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
    data1 = zip(list_b, time_order, visit_b, time_match)
    matched_timetable = pd.DataFrame(data=data1, columns=["SubjectID", "VisitTime", "Castor_Date", "Match_Date"])

    # step 4 append guid to sub+castor+match device with key sub+device date
    sub_id = sub["SubjectID"].to_list()
    guid_list = sub["ImgCollGUID"].to_list()
    sub_visit = sub["VisitDate"].to_list()
    sub_cri = []
    for i in range(len(sub_id)):
        cri = str(sub_id[i]) + " " + str(sub_visit[i])
        sub_cri.append(cri)
    data = zip(sub_cri, guid_list)
    df = pd.DataFrame(data=data, columns=["sub_time", "guid"])
    df1 = df.groupby('sub_time', group_keys=False)['guid'].apply(list).reset_index(name='new')
    df1.to_excel("/Users/ziweishi/Downloads/check1.xlsx")

    list_sub = matched_timetable["SubjectID"].to_list()
    list_time1 = matched_timetable["Match_Date"].to_list()
    list_time = []
    for i in list_time1:
        if len(i) > 0:
            i = str(i)
            # i = i.strip('][').split(',')
            i = i.replace("'", "")
            i = i.replace(" ", "")
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
    subjectid_list = []
    visitime_list = []
    guid_final_list = []
    capture_date = []
    castor_date = []

    num_list = []
    total_none_match = 0
    sub_status = []

    none_match_subject = []
    none_match_guid = []
    none_cap_date = []

    for i in range(len(list_com)):
        subjectid = list_b[i]
        visit_time = time_order[i]
        sta = status[subjectid]
        sub_status.append(sta)
        list_guid_pic = []  # 创建用于存储所有迭代结果的列表

        for j in list_com[i]:
            try:
                sub_set = df1[df1["sub_time"] == j]
                value_list = sub_set["new"].iloc[0]
                # print(len(value_list))
                for r in value_list:
                    list_guid_pic.append(r)
            except:
                list_guid_pic = list_guid_pic

        num = len(list_guid_pic)

        list_guid.append(list_guid_pic)

        num_list.append(num)
        if "none" in visit_time:
            total_none_match += num
            for u in list_guid_pic:
                none_match_subject.append(subjectid)
                none_match_guid.append(u)
                none_date_set = sub[sub["ImgCollGUID"] == h]
                none_date = none_date_set["VisitDate"].iloc[0]
                none_cap_date.append(none_date)

        # add guid to output matched guid file
        if "none" not in visit_time:
            for h in list_guid_pic:
                subjectid_list.append(subjectid)
                visitime_list.append(visit_time)
                guid_final_list.append(h)
                cap_date_set = sub[sub["ImgCollGUID"] == h]
                cap_date = cap_date_set["VisitDate"].iloc[0]
                capture_date.append(cap_date)
                castor_date.append(visit_b[i])

    # output guid list
    list_file_name = str(update_date) + "_Guid_list.xlsx"
    list_final_path = os.path.join(path, list_file_name)
    final_guid = zip(subjectid_list, visitime_list, castor_date, capture_date, guid_final_list)

    check_type = ["PseudoColor", "Assessing", "Mask", "phase", "Tags", "Status"]

    source_info = {i: [] for i in check_type}
    server_info = []

    index = 0
    collection_type = []
    status_final = []
    out_num = 0
    for i in guid_final_list:
        sub_source = db_source[db_source["ImgCollGUID"] == i]
        server_source = sub[sub["ImgCollGUID"] == i]
        local_path = server_source["ImageCollFolderName"].iloc[0]
        server_info.append(local_path)
        for s in check_type:
            try:
                value = sub_source[s].iloc[0]
                source_info[s].append(value)
            except:
                source_info[s].append(np.nan)

        subject = subjectid_list[index]
        sta = status[subject]
        status_final.append(sta)
        castor_time = castor_date[index]
        if subject in issue:
            issue_list = issue[subject]
            if castor_time in issue_list:
                collection_type.append("out of 12 weeks")
                out_num += 1
            else:
                collection_type.append(np.nan)
        else:
            collection_type.append(np.nan)
        index += 1

    final_guid_df = pd.DataFrame(final_guid,
                                 columns=["SubjectID", "VisitTime", "Castor_Date", "Capture_Date", "ImgCollGUID"])
    final_guid_df["Complete_Status"] = status_final
    final_guid_df["12 Weeks Check"] = collection_type
    final_guid_df["ImageCollFolderName"] = server_info

    for y in check_type:
        final_guid_df[y] = source_info[y]
    final_guid_df.to_excel(list_final_path)
    final_guid_df.to_excel("../Documents/dfu_latest_match_validation.xlsx")
    print("total matched guid num: " + str(len(guid_final_list)))
    print("total non-matched guid num: " + str(total_none_match))
    print("total out off 12 weeks guid num: " + str(out_num))

    list_download_name = str(update_date) + "_download_list.xlsx"
    list_download_path = os.path.join(path, list_download_name)
    final_download_df = final_guid_df[final_guid_df["phase"].isna()]
    final_download_df.to_excel(list_download_path)
    final_download_df.to_excel("../Documents/download_file/val_download_list.xlsx")

    final_none_match = zip(none_match_subject, none_match_guid, none_cap_date)
    final_none_df = pd.DataFrame(final_none_match, columns=["SubjectID", "ImgCollGUID", "VisitTime"])
    list_none_name = str(update_date) + "_none_match_list.xlsx"
    list_none_path = os.path.join(path, list_none_name)
    final_none_df.to_excel(list_none_path)

    # output match situation frame
    match_file_name = str(update_date) + "_matched_Guid.xlsx"
    match_final_path = os.path.join(path, match_file_name)
    data_guid = zip(list_b, sub_status, time_order, visit_b, time_match, num_list, list_guid)
    df_final = pd.DataFrame(data=data_guid,
                            columns=["SubjectID", "Complete_Status", "VisitTime", "Castor_Date", "Match_Device_Date",
                                     "Num_GUID", "ImgCollGUID"])
    df_final.to_excel(match_final_path)
    return df_final



if __name__ == "__main__":
    # a = input("Do you use the latest WAUSI Enrollment tracker file?")
    training_time_table_transfer("20230905tra")
    validation_time_table_transfer("20230905val")

