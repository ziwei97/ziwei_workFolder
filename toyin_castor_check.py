import pandas as pd
import numpy as np
from datetime import datetime


def clean_track(check_date):
    toyin = pd.read_excel("/Users/ziweishi/Desktop/WAUSI.xlsx")
    df_toyin = pd.DataFrame()
    df_toyin["SubjectID"] = toyin["Subject ID"]
    df_toyin["status"] = toyin["Completed Study (or withdrawn/LTF)"]
    df_toyin["Data Type"] = toyin["Data Type"]
    column = ["SubjectID"]

    def change_format(date):
        i = str(date)

        try:
            if "." in i:
                i = datetime.strptime(i, "%m.%d.%y").strftime("%d-%m-%Y")
            if "/" in i:
                i = datetime.strptime(i, "%m/%d/%y").strftime("%d-%m-%Y")
            if "-" in i:
                try:
                    i = datetime.strptime(i, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
                except:
                    i = datetime.strptime(i, "%d-%m-%Y").strftime("%d-%m-%Y")

            if i =="No EDC data":
                i = np.nan
            if i =="?":
                i = np.nan
        except:
            i = date
            print(i)
        return i

    for i in range(1, 13):

        if i ==1:
            visit = "SV_" + str(i) + "_Date"

            to_vis = "BSV/SV1"
            column.append(visit)
            date_time_list = []
            for j in toyin[to_vis]:
                if type(j) != float and str(j) != "NaT":
                    j = change_format(j)
                    date_time_list.append(j)
                else:
                    date_time_list.append(np.nan)
            visit_date = pd.DataFrame(date_time_list)
            df_toyin[visit] = visit_date
        else:
            visit = "SV_" + str(i) + "_Date"

            to_vis = "SV" + str(i)
            column.append(visit)
            date_time_list = []
            for j in toyin[to_vis]:
                # print(j)
                # print(type(j))
                if type(j) != float and str(j) != "NaT":
                    j = change_format(j)
                    date_time_list.append(j)

                else:
                    date_time_list.append(np.nan)
            visit_date = pd.DataFrame(date_time_list)
            df_toyin[visit] = visit_date


    df_toyin["Data Type"] = toyin["Data Type"]
    status = ["Completed","Completed (LTF)","Withdrawn (SAE)"]
    df_toyin = df_toyin[df_toyin["status"].isin(status)]
    df_toyin = df_toyin[df_toyin["Data Type"]=="Training data"]

    issue ={}
    issue["202-018"]=["09-11-2022","21-11-2022"]
    issue["202-020"] = ["22-11-2022"]
    issue["202-023"] = ["21-12-2022"]
    issue["202-029"] = ["30-01-2022"]
    issue["202-030"] = ["24-01-2023","31-01-2023"]


    subject_list = df_toyin["SubjectID"].to_list()
    status_list = df_toyin["status"].to_list()

    sub_sta ={}
    index=0
    for i in subject_list:
        sub_sta[i] = status_list[index]
        index+=1



    path = "/Users/ziweishi/Documents/DFU_regular_update/"+check_date+"/toyin_filtered.xlsx"
    df_toyin.to_excel(path)

    return df_toyin,issue,sub_sta


if __name__ == "__main__":
    clean_track("2022065")
