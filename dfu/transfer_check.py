import os.path
import pymysql
import pandas as pd
import numpy as np
import get_sql_from_smb as sql_get
from util import download_whole_dynamodb_table

#refresh device database with the latest database sql file
def refresh_sql_database(check_list):
    local_site = ["nynw", "ocer", "whfa", "youngst", "lvrpool", "memdfu", "hilloh", "grovoh", "mentoh", "encinogho",
                  "lahdfu"]
    s3_site = ["rsci"]
    site_list = {}
    for i in check_list:
        site_list[i] = {}
        if i in local_site:
            site_list[i]["type"] = "local"
        elif i in s3_site:
            site_list[i]["type"] = "s3"
        else:
            print("wrong site")

    sql_info = sql_get.dfu_sql_find(site_list)
    sql_path = sql_info[0]
    b = sql_info[1]


    for i in check_list:
        site_list[i]["sql_path"] = sql_path[i]
        print(i+" "+sql_path[i])
        if b == "yes":
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='szw970727',
                database=i,
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = connection.cursor()

            # 打开SQL文件并执行其中的SQL语句
            with open(sql_path[i], 'r') as sql_file:
                sql_statements = sql_file.read().split(';')
                for statement in sql_statements:
                    if statement.strip():
                        cursor.execute(statement)
            # 提交更改
            connection.commit()
            cursor.close()
            connection.close()

    a = input("is the path right? ")
    if a !="no":
        return site_list
    else:
        return False



def has_element(value,element_list):
    for i in element_list:
        if i in value:
            return True
    return False

def parse_date(x):
    try:
        stamp = int(x) - 2209031999999999700 - 6*60*60*1000000000
        eval = str(pd.to_datetime(stamp).strftime('%d-%m-%Y'))
    except:
        eval = np.nan
    return eval


#running select join in each site database
def server_table_output(sql_path,site):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='szw970727',
        database=site,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()

    query1 = "select * from imagescollection left join injury on imagescollection.INJURYID = injury.INJURYID left join patient on injury.PID = patient.PID"
    cursor.execute(query1)
    collection_result = cursor.fetchall()
    df = pd.DataFrame(collection_result)
    df["CaptureDate"]=df["CreateDateTime"].apply(lambda x: str(x))


    query2 = "select * from imagescollection left join images on imagescollection.IMCOLLID=images.IMCOLLID"
    cursor.execute(query2)
    image_result = cursor.fetchall()
    df2 = pd.DataFrame(image_result)
    info = sql_path.split("/")[-1]
    date = info.split("_")[-2]
    site = info.split("_")[-3]
    site_path = '/Users/ziweishi/Documents/transfer_regular_check/'+site+"/"
    if os.path.isdir(site_path)==False:
        os.mkdir(site_path)
    check_path = site_path+date+"/"
    if os.path.isdir(check_path)==False:
        os.mkdir(check_path)

    og_file_path = check_path + site + "_" + date + "_collection_og.xlsx"
    df.to_excel(og_file_path)

    if site != "memdfu":
        element_list = ["000", "99","8888"]
    else:
        element_list = ["0000", "99"]


    df = df[~df["MedicalNumber"].apply(lambda x: has_element(x, element_list))]

    if site == "whfa":
        df["MedicalNumber"] = df["MedicalNumber"].apply(lambda x: "203-" + x)
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("-203", "-005") if "-203" in x else x)
    if site == "lvrpool":
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("105", "205") if "105" in x else x)
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("205", "205-") if "205" in x else x)
    if site == "encinogho":
        df["MedicalNumber"] = df["MedicalNumber"].apply(lambda x: "210-" + x if "210" not in x else x)
    if site == "ocer":
        df["MedicalNumber"] = df["MedicalNumber"].apply(lambda x: "202-" + x if "202" not in x else x)
    if site == "youngst":
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("204", "204-") if "204" in x else x)
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: "204-" + x if "204-" not in x else x)
    if site == "memdfu":
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("00067469", "206-008") if "00067469" in x else x)
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("00038523", "206-009") if "00038523" in x else x)
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("02042426", "206-010") if "02042426" in x else x)
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: "206-" + x if "206-" not in x else x)
    if site == "lahdfu":
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: x.replace("211-01", "211-001") if "211-01" in x else x)
    if site == "rsci":
        df["MedicalNumber"] = df["MedicalNumber"].apply(
            lambda x: "292-" + x if "292-" not in x else x)

    guid_file_path = check_path+site+"_"+date+"_collection.xlsx"
    df.to_excel(guid_file_path, index=False)

    image_file_path = check_path+site+"_"+date+"_image.xlsx"
    df2.to_excel(image_file_path,index=False)

    cursor.close()
    connection.close()
    return df,df2,site,check_path

#check guid exist in cloud
def guid_check(db,df,site,check_path):
    check_list = df["ImgCollGUID"].to_list()
    db_list = db["ImgCollGUID"].to_list()
    index=0
    issue_guid=[]
    success_guid=[]
    status=[]
    folder=[]
    subject_id=[]
    for i in check_list:
        df_sub = df[df["ImgCollGUID"] == i]
        location = df_sub["ImageCollFolderName"].iloc[0]
        subject = df_sub["MedicalNumber"].iloc[0]
        folder.append(location)
        subject_id.append(subject)
        if i in db_list:
            success_guid.append(i)
            status.append("exist")
            index+=0
        else:
            issue_guid.append(i)
            index+=1
            status.append("new")
    if index==0:
        print(site+": "+"all check!")
    else:
        print(site+": "+str(len(issue_guid))+"/"+str(len(check_list)))
    data = zip(check_list,subject_id, status,folder)
    df_guid = pd.DataFrame(data, columns=["ImgCollGUID", "SubjectID","Transfer_Status","File_Location"])
    file_name =site+"_guid_log_out.xlsx"
    status_file = os.path.join(check_path,file_name)
    df_guid.to_excel(status_file)
    return df_guid

#check image exist in cloud
def image_check(db,df,df2,site,check_path):
    df_guid = guid_check(db,df,site,check_path)
    guid = df_guid["ImgCollGUID"].to_list()
    status={}
    site_info=[]
    for i in guid:
        site_info.append(site)
        comment={}
        df_sub = df2[df2["ImgCollGUID"]==i]
        db_sub = db[db["ImgCollGUID"] == i]
        # check if raw in db
        if len(db_sub)==0:
            comment["Raw Issue"] = "no guid"
            comment["Pseudo Issue"] ="no guid"
            comment["Assessing Issue"] = "no guid"
            comment["Reference Issue"] = "no guid"
        else:
            # check if pseudo in db
            raw_sub = df_sub[df_sub["ImageType"] == "Raw MSI"]
            raw_list = raw_sub["ImageFileName"].to_list()
            if len(raw_list) > 0:
                try:
                    db_raw = db_sub["Raw"].iloc[0]
                    db_raw1 = db_raw.replace(" ", "")

                    db_raw1 = db_raw1.replace("Raw/Raw_", "")
                    db_raw1 = db_raw1.replace("'", "")

                    db_raw2 = db_raw1.strip("{}").split(",")

                    issue_list = []
                    for p in raw_list:
                        if p not in db_raw2:
                            issue_list.append(p)
                    if len(issue_list) > 0:
                        comment["Raw Issue"] = issue_list
                    else:
                        comment["Raw Issue"] = np.nan
                except:
                    comment["Raw Issue"] = "db no raw"

            else:
                comment["Raw Issue"] = "lc lost raw"



            # check if pseudo in db
            pseudo_sub = df_sub[df_sub["ImageType"] == "Pseudocolor"]
            pseudo_list = pseudo_sub["ImageFileName"].to_list()
            if len(pseudo_list)>0:
                try:
                    db_pseudo = db_sub["PseudoColor"].iloc[0]
                    db_pseudo1 = db_pseudo.replace("PseudoColor/", "")
                    db_pseudo1 = db_pseudo1.replace(" ", "")
                    db_pseudo1 = db_pseudo1.replace("'", "")
                    db_pseudo2 = db_pseudo1.strip("{}").split(",")
                    if len(pseudo_list) != len(db_pseudo2):
                        comment["Pseudo Issue"] = "wrong pseudo"
                    else:
                        comment["Pseudo Issue"] = np.nan
                except:
                    comment["Pseudo Issue"] = "db no pseudo"
            else:
                comment["Pseudo Issue"] = "lc lost pseudo"



            # check if assessing in db
            assessing_sub = df_sub[df_sub["ImageType"] == "CJA"]
            assessing_list = assessing_sub["ImageFileName"].to_list()
            if len(assessing_list)>0:
                try:
                    db_assessing = db_sub["Assessing"].iloc[0]
                    db_assessing1 = db_assessing.replace("Assessing/", "")
                    db_assessing1 = db_assessing1.replace(" ", "")
                    db_assessing1 = db_assessing1.replace("'", "")
                    db_assessing2 = db_assessing1.strip("{}").split(",")

                    if len(assessing_list) != len(db_assessing2):
                        comment["Assessing Issue"] = "wrong assessing"
                    else:
                        comment["Assessing Issue"] = np.nan
                except:
                    comment["Assessing Issue"] = "db no assessing"

            else:
                comment["Assessing Issue"] = "lc lost assessing"


            # check if reference in db
            reference_sub = df_sub[df_sub["ImageType"] == "Reference"]
            reference_list = reference_sub["ImageFileName"].to_list()
            if len(reference_list)>0:
                try:
                    db_reference = db_sub["Reference"].iloc[0]
                    db_reference1 = db_reference.replace("Reference/", "")
                    db_reference1 = db_reference1.replace(" ", "")
                    db_reference1 = db_reference1.replace("'", "")
                    db_reference2 = db_reference1.strip("{}").split(",")
                    for z in db_reference2:
                        if "." not in z:
                            db_reference2.remove(z)
                    if len(reference_list) != len(db_reference2):
                        comment["Reference Issue"] = "wrong reference"
                    else:
                        comment["Reference Issue"] = np.nan
                except:
                    comment["Reference Issue"] = "db no reference"
            else:
                comment["Reference Issue"] = "lc lost reference"


        status[i] = comment

    raw_issue_list=[]
    pseudo_issue_list=[]
    assessing_issue_list=[]
    reference_issue_list=[]

    for j in guid:
        issue = status[j]
        raw_issue_list.append(issue["Raw Issue"])
        pseudo_issue_list.append(issue["Pseudo Issue"])
        assessing_issue_list.append(issue["Assessing Issue"])
        reference_issue_list.append(issue["Reference Issue"])

    df_guid["Raw Issue"]=raw_issue_list
    df_guid["Pseudo Issue"] = pseudo_issue_list
    df_guid["Assessing Issue"] = assessing_issue_list
    df_guid["Reference Issue"]=reference_issue_list
    df_guid["Site"]=site_info

    file_name = site + "_image_log_out.xlsx"
    image_status_file = os.path.join(check_path, file_name)
    df_guid.to_excel(image_status_file)
    return df_guid




if __name__ =="__main__":


    # local_site = ["nynw", "ocer", "whfa", "youngst", "lvrpool", "memdfu", "hilloh", "grovoh", "mentoh", "encinogho","lahdfu","rsci"]
    check_site = [ "nynw", "ocer", "whfa", "youngst", "lvrpool", "memdfu", "hilloh", "grovoh", "mentoh", "encinogho","lahdfu","rsci"]
    check_list = {}

    site_list = refresh_sql_database(check_site)
    if site_list !=False:
        for check in check_site:
            check_list[check] = site_list[check]

        db = download_whole_dynamodb_table.download_table("DFU_Master_ImageCollections")
        db = db[db["StudyName"] == "DFU_SSP"]

        data_sites = []
        for i in check_list.keys():
            path = check_list[i]["sql_path"]
            df_guid, df_image, site, check_path = server_table_output(path,i)
            site_image = image_check(db, df_guid, df_image, site, check_path)
            data_sites.append(df_guid)

        union_df = pd.concat(data_sites)
        union_df.to_excel("/Users/ziweishi/Desktop/dfu_site_check.xlsx")

    else:
        print("Wrong Path!")














