from collections import Counter
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import transfer_check
import pandas as pd
import numpy as np


def output_total():
    a = input("new output?")
    if a =="yes":
        check_site = ["nynw", "ocer", "whfa", "youngst", "lvrpool", "memdfu", "hilloh", "grovoh", "mentoh",
                      "encinogho", "lahdfu", "rsci"]
        site_list = transfer_check.refresh_sql_database(check_site)
        if site_list != False:
            check_list = {}
            for check in check_site:
                check_list[check] = site_list[check]
            data_sites = []
            for i in check_list.keys():
                path = check_list[i]["sql_path"]
                df_guid, df_image, site, check_path = transfer_check.server_table_output(path, i)
                data_sites.append(df_guid)
            union_df = pd.concat(data_sites)
            union_df.to_excel("/Users/ziweishi/Desktop/dfu_check.xlsx")
            return union_df
        else:
            print("Wrong Path!")
    else:
        df = pd.read_excel("/Users/ziweishi/Desktop/dfu_check.xlsx")
        return df



def subject_info():
    tr_src =  pd.read_excel("/Users/ziweishi/Downloads/WAUSI.xlsx", sheet_name="Training Dataset")
    vd_src = pd.read_excel("/Users/ziweishi/Downloads/WAUSI.xlsx", sheet_name="Validation Dataset")

    tr = pd.DataFrame()
    tr["MedicalNumber"]=tr_src["Subject ID"].to_list()
    tr["Status"]= tr_src["Completed Study (or withdrawn/LTF)"].to_list()
    tr["site"] = tr["MedicalNumber"].apply(lambda x: x[0:3])
    tr_info={"201":"nynw","202":"ocer","203":"whfa","204":"youngst","205":"lvrpool","292":"rcsi"}
    tr["site_name"] = tr["site"].apply(lambda x: tr_info[x])
    tr["type"]="training"

    vd = pd.DataFrame()
    vd["MedicalNumber"] = vd_src["Subject ID"].to_list()
    vd["Status"] = vd_src["Completed Study (or withdrawn/LTF)"].to_list()
    vd["site"] = vd["MedicalNumber"].apply(lambda x: x[0:3])
    vd_info = { "206": "memdfu", "207": "hilloh", "208": "grovoh","209":"mentoh",
               "210":"encinogho","211":"lahdfu"}
    vd["site_name"] = vd["site"].apply(lambda x: vd_info[x])
    vd["type"] = "validation"

    total = [tr,vd]

    df = pd.concat(total)

    df.to_excel("/Users/ziweishi/Desktop/wausi_subject.xlsx")
    return df



def make_summary(cur_date):
    # df_type = pd.read_excel("/Users/ziweishi/Desktop/wausi_subject.xlsx",sheet_name="total")
    df_type = subject_info()
    df_guid = output_total()
    df = pd.merge(df_type,df_guid,on="MedicalNumber",how="left")
    df = df[df["ImgCollGUID"].notna()]
    # df.to_excel("/Users/ziweishi/Desktop/check.xlsx")

    df_tra = df[df["type"]=="training"]
    df_tra = df_tra.copy()
    df_tra["site"] = df_tra["site"].apply(lambda x: str(x))

    tra_img_total = df_tra["MedicalNumber"].to_list()
    tra_sub_image_count = Counter(tra_img_total)
    tra_img_sum = pd.DataFrame(list(tra_sub_image_count.items()), columns=["SubjectID", "Image_Num"])

    tra_sub = tra_sub_image_count.keys()
    tra_site_ab = [x[0:3] for x in tra_sub]
    tra_site_info = {}
    for i in tra_sub:
        sub_tra = tra_img_sum[tra_img_sum["SubjectID"] == i]
        num = sub_tra["Image_Num"].iloc[0]
        ii = i[0:3]
        if ii not in tra_site_info:
            tra_site_info[ii] = num
        else:
            tra_site_info[ii] += num

    tra_site_num = Counter(tra_site_ab)
    tra_site_sum = pd.DataFrame(list(tra_site_num.items()), columns=["Site", "Sub_Num"])
    tra_site_list = tra_site_sum["Site"].to_list()

    tra_sum = []
    tra_site_name = []

    for j in tra_site_list:
        tra_sub_info = df_tra[df_tra["site"] == j]
        j_name = tra_sub_info["site_name"].iloc[0]
        sum_num = tra_site_info[j]
        tra_sum.append(sum_num)
        tra_site_name.append(j_name)

    tra_site_sum["Img_Sum"] = tra_sum
    tra_site_sum["Site_Name"] = tra_site_name

    tra_total ={}
    tra_total["Site"] = "total"
    tra_total["Sub_Num"] = len(tra_sub)
    tra_total["Img_Sum"] = len(tra_img_total)
    tra_total["Site_Name"]=np.nan
    df_tra_total = pd.DataFrame(tra_total,index=[0])
    df_tra_list = [tra_site_sum,df_tra_total]
    df_tra_final = pd.concat(df_tra_list)


    df_val = df[df["type"] == "validation"]
    df_val = df_val.copy()
    df_val["site"] = df_val["site"].apply(lambda x: str(x))

    val_img_total = df_val["MedicalNumber"].to_list()
    val_sub_image_count = Counter(val_img_total)
    val_img_sum = pd.DataFrame(list(val_sub_image_count.items()), columns=["SubjectID", "Image_Num"])


    val_sub = val_sub_image_count.keys()
    val_site_ab = [x[0:3] for x in val_sub]
    val_site_info = {}
    for i in val_sub:
        sub_val = val_img_sum[val_img_sum["SubjectID"] == i]
        num = sub_val["Image_Num"].iloc[0]
        ii = i[0:3]
        if ii not in val_site_info:
            val_site_info[ii] = num
        else:
            val_site_info[ii] += num

    val_site_num = Counter(val_site_ab)
    val_site_sum = pd.DataFrame(list(val_site_num.items()), columns=["Site", "Sub_Num"])
    val_site_list = val_site_sum["Site"].to_list()

    val_sum = []
    val_site_name = []

    for j in val_site_list:
        val_sub_info = df_val[df_val["site"] == j]
        j_name = val_sub_info["site_name"].iloc[0]
        sum_num = val_site_info[j]
        val_sum.append(sum_num)
        val_site_name.append(j_name)

    val_site_sum["Img_Sum"] = val_sum
    val_site_sum["Site_Name"] = val_site_name

    val_total = {}
    val_total["Site"] = "total"
    val_total["Sub_Num"] = len(val_sub)
    val_total["Img_Sum"] = len(val_img_total)
    val_total["Site_Name"] = np.nan

    df_val_total = pd.DataFrame(val_total,index=[0])
    df_val_list = [val_site_sum, df_val_total]
    df_val_final = pd.concat(df_val_list)

    file = "WAUSI_Summary_" + cur_date + ".xlsx"
    path = "/Users/ziweishi/Desktop/DFU_Summary/" + file

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df_tra_final.to_excel(writer, sheet_name='training_site_summary', index=False)
    tra_img_sum.to_excel(writer, sheet_name='training_subject_summary', index=False)
    df_val_final.to_excel(writer, sheet_name='validation_site_summary', index=False)
    val_img_sum.to_excel(writer, sheet_name='validation_subject_summary', index=False)

    writer.close()


    workbook =load_workbook(path)

    # 对每个 sheet 设置单元格居中
    for sheet in workbook.sheetnames:
        ws = workbook[sheet]
        for row in ws.iter_rows():
            for cell in row:
                cell.alignment = Alignment(horizontal='center', vertical='center')

    # 保存更改后的 Excel 文件

    workbook.save(path)


if __name__ =="__main__":
    # make_summary("080123")
    output_total()
