import pandas as pd
from datetime import datetime, timedelta
import download_whole_dynamodb_table
import numpy as np

guid= download_whole_dynamodb_table.get_table('DFU_Master_ImageCollections')
guid = pd.DataFrame(guid)
guid_list = guid[['SubjectID','ImgCollGUID','CreateTimeStamp','Status']]
guid_list = guid_list[guid_list["Status"]=="acquired"]
guid_list = guid_list[guid_list["CreateTimeStamp"].notna()]

def parse_date(x):
    try:
        stamp = int(x) - 2209031999999999700
        eval = str(pd.to_datetime(stamp).strftime('%d-%m-%Y'))
    except:
        eval = np.nan
    return eval

guid_list["VisitDate"] = guid_list[["CreateTimeStamp"]].apply(lambda x: parse_date((x['CreateTimeStamp'])), axis=1)
guid_list[['SubjectID','ImgCollGUID','VisitDate']].to_excel("/Users/ziweishi/Desktop/DFU/GUID_Match/Subject_Guid_Time.xlsx")


phase_list1 =  pd.read_excel("/Users/ziweishi/Desktop/DFU/GUID_Match/WAUSI_Subject_Conclusion.xlsx",sheet_name="phase1")
phase1 = phase_list1["SubjectID"].to_list()

phase_list2 =  pd.read_excel("/Users/ziweishi/Desktop/DFU/GUID_Match/WAUSI_Subject_Conclusion.xlsx",sheet_name="phase2")
phase2 = phase_list2["SubjectID"].to_list()


castor_report_total = pd.read_csv("/Users/ziweishi/Desktop/DFU/GUID_Match/US_Wound_Assessment_Using_Spec_export_20230313.csv")
#
# column_name = ["Participant Id","Participant Status","Site Abbreviation","BSV_Date"]
#
# for i in range(2, 13):
#     time_type = "SV"+ str(i) + "_SV_Date"
#     column_name.append(time_type)
#
# print(column_name)
#
# castor_report_select = castor_report_total.loc[:,column_name]





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


def time_table_transfer(visit_report_path,guid_file_path):
    vt = pd.read_excel(visit_report_path)
    sub = pd.read_excel(guid_file_path)

    vt_sub = vt["SubjectID"].to_list()
    list_b = []
    time_order = []
    visit_b = []
    time_match = []

    for i in vt_sub:
        for j in range(1, 13):
            time_type = "SV_" + str(j) + "_Date"
            vt_subset = vt[vt["SubjectID"] == i]
            time_v = vt_subset[time_type].iloc[0]
            list_b.append(i)
            time_order.append(time_type)
            visit_b.append(time_v)

    data = zip(list_b, time_order, visit_b)
    time_table = pd.DataFrame(data=data, columns=["SubjectID", "VisitTime", "Castor_Date"])


    for j in vt_sub:
        sub_set = sub[sub["SubjectID"] == j]
        time_set = time_table[time_table["SubjectID"] == j]
        sub_dates = sub_set["VisitDate"].to_list()
        sub_date = [k for k in sub_dates]
        time_date = time_set["Castor_Date"].to_list()

        for x in time_date:
            date_list = []
            for y in sub_date:
                if fuzzy_date_match(x, y, 2, date_format='%d-%m-%Y') == True:
                    if y not in date_list:
                        date_list.append(y)
            time_match.append(date_list)


    data1 = zip(list_b, time_order, visit_b,time_match)
    matched_timetable = pd.DataFrame(data=data1, columns=["SubjectID", "VisitTime", "Castor_Date","Match_Date"])


    sub_id = sub["SubjectID"].to_list()
    guid_list = sub["ImgCollGUID"].to_list()
    sub_visit1 = sub["VisitDate"].to_list()
    sub_visit = [i for i in sub_visit1]

    sub_cri = []
    for i in range(len(sub_id)):
        date = sub_visit[i]
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
            i = i.replace("'", "")
            i = i.replace("[", "")
            i = i.replace("]", "")
            i = i.split(",")

        list_time.append(i)
    # print(list_time)
    list_com = []

    for i in range(len(list_sub)):
        x = list_sub[i]
        list_pic = []
        for j in list_time[i]:
            p = str(x) + " " + str(j)
            list_pic.append(p)
        list_com.append(list_pic)

    list_guid = []
    for i in range(len(list_com)):
        list_guid_pic = []
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


    data_guid = zip(list_b, time_order, visit_b, time_match, list_guid)
    df_final = pd.DataFrame(data=data_guid,columns=["SubjectID", "VisitTime", "Castor_Date", "Match_Device_Date", "ImgCollGUID"])

    return df_final


# final_list = time_table_transfer("/Users/ziweishi/Desktop/DFU/GUID_Match/phase2_report_20230313.xlsx","/Users/ziweishi/Desktop/DFU/GUID_Match/Subject_Guid_Time.xlsx")
# final_list.to_excel("/Users/ziweishi/Desktop/DFU/GUID_Match/Matched_Guid_Time2.xlsx")