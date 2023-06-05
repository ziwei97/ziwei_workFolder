import os.path

import pymysql
import pandas as pd
import numpy as np

import download_whole_dynamodb_table


def server_table_output(sql_path):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='szw970727',
        database='algorithm',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    path =sql_path
    with open(path, 'r') as file:
        query = file.read()

    statements = query.split(';')
    # Execute each statement
    for statement in statements:
        cursor.execute(statement)


    query1 = "select * from imagescollection left join injury on imagescollection.INJURYID=injury.INJURYID join patient on injury.PID = patient.PID"
    cursor.execute(query1)
    collection_result = cursor.fetchall()
    df = pd.DataFrame(collection_result)

    query2 = "select * from imagescollection left join images on imagescollection.IMCOLLID=images.IMCOLLID"
    cursor.execute(query2)
    image_result = cursor.fetchall()
    df2 = pd.DataFrame(image_result)

    date = ((sql_path.split("/"))[-3])[-8:]
    site = (sql_path.split("/"))[-5]
    site_path = '/Users/ziweishi/Documents/transfer_regular_check/'+site+"/"
    if os.path.isdir(site_path)==False:
        os.mkdir(site_path)
    check_path = site_path+date+"/"
    if os.path.isdir(check_path)==False:
        os.mkdir(check_path)
    guid_file_path = check_path+"collection.xlsx"
    df.to_excel(guid_file_path, index=False)

    image_file_path = check_path+ "image.xlsx"
    df2.to_excel(image_file_path,index=False)

    cursor.close()
    connection.close()
    return df,df2,site,check_path


def guid_check(df,site,check_path):
    db = download_whole_dynamodb_table.download_table("DFU_Master_ImageCollections")
    db = db[db["StudyName"]=="DFU_SSP"]
    check_list = df["ImgCollGUID"].to_list()
    print("total guid in "+site+" transfer is "+str(len(check_list)))
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
        print("all check!")
    else:
        print("total guid in "+site+" non-transfer is "+str(len(issue_guid)))
    data = zip(check_list,subject_id, status,folder)
    df_guid = pd.DataFrame(data, columns=["ImgCollGUID", "SubjectID","Transfer_Status","File_Location"])
    status_file = os.path.join(check_path,"guid_log_out.xlsx")
    df_guid.to_excel(status_file)
    return df_guid,db


def image_check(df,df2,site,check_path):
    df_guid,db = guid_check(df,site,check_path)
    guid = df_guid["ImgCollGUID"].to_list()
    status={}
    for i in guid:
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
            try:
                raw_sub = df_sub[df_sub["ImageType"] == "Raw MSI"]
                raw_list = raw_sub["ImageFileName"].to_list()
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
                comment["Raw Issue"] = "no raw"

            # check if pseudo in db
            try:
                pseudo_sub = df_sub[df_sub["ImageType"] == "Pseudocolor"]
                pseudo_list = pseudo_sub["ImageFileName"].to_list()
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
                comment["Pseudo Issue"] = "no pseudo"
            # check if assessing in db
            try:
                assessing_sub = df_sub[df_sub["ImageType"] == "CJA"]
                assessing_list = assessing_sub["ImageFileName"].to_list()
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
                comment["Assessing Issue"] = "no assessing"

            # check if reference in db
            try:
                reference_sub = df_sub[df_sub["ImageType"] == "Reference"]
                reference_list = reference_sub["ImageFileName"].to_list()
                db_reference = db_sub["Reference"].iloc[0]
                db_reference1 = db_reference.replace("Reference/", "")
                db_reference1 = db_reference1.replace(" ", "")
                db_reference1 = db_reference1.replace("'", "")
                db_reference2 = db_reference1.strip("{}").split(",")
                if len(reference_list) != len(db_reference2):
                    comment["Reference Issue"] = "wrong reference"
                else:
                    comment["Reference Issue"] = np.nan
            except:
                comment["Reference Issue"] = "no reference"
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


    image_status_file = os.path.join(check_path, "image_log_out.xlsx")
    df_guid.to_excel(image_status_file)




if __name__ =="__main__":
    site_loc = {
        "nynw":"/Volumes/dfu/DataTransfers/nynw/DFU_SS/NYNW_DFU_SMD2223-008_04_11_23/SpectralView/dvsspdata.sql",
        # "ocer":"/Volumes/dfu/DataTransfers/ocer/DFU_SS/OCER_DFU_SMD2148-019_04_25_23/SpectralView/dvsspdata.sql",
        # "whfa":"/Volumes/dfu/DataTransfers/whfa/DFU_SS/WHFA_DFU_SMD2223-007_04_11_23/SpectralView/dvsspdata.sql",
        # "youngst":"/Volumes/dfu/DataTransfers/youngst/DFU_SS/YOUNGST_DFU_SMD2223-010_03_20_23/SpectralView/dvsspdata.sql",
        # "lvrpool":"/Volumes/dfu/DataTransfers/lvrpool/DFU_SS/LVRPOOL_DFU_SMD2223-009-03_20_23/SpectralView/dvsspdata.sql",
        # "hilloh":"/Volumes/dfu/DataTransfers/hilloh/DFU_SS/HILLOH_DFU_SMD2225-011_04_25_23/SpectralView/dvsspdata.sql",
        # "grovoh":"/Volumes/dfu/DataTransfers/grovoh/DFU_SS/GROVOH_DFU_SMD2225-013_04_25_23/SpectralView/dvsspdata.sql",
        # "mentoh":"/Volumes/dfu/DataTransfers/mentoh/DFU_SS/MENTOH_DFU_SMD2223-007_06_01_23/SpectralView/dvsspdata.sql",
        # "encinogho":"/Volumes/dfu/DataTransfers/encinogho/DFU_SS/ENCINO_DFU_SMD2225-018_05_15_23/SpectralView/dvsspdata.sql"
    }
    site_list=site_loc.keys()
    for i in site_list:
        path = site_loc[i]
        df_guid, df_image, site, check_path = server_table_output(path)
        image_check(df_guid, df_image, site, check_path)




