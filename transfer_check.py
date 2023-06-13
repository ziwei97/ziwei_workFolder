import os.path

import pymysql
import pandas as pd
import numpy as np

import download_whole_dynamodb_table

def has_element(value,element_list):
    for i in element_list:
        if i in value:
            return True

    return False



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

    element_list = ["000", "99"]
    df = df[~df["MedicalNumber"].apply(lambda x: has_element(x, element_list))]

    guid_file_path = check_path+"collection.xlsx"
    df.to_excel(guid_file_path, index=False)

    image_file_path = check_path+ "image.xlsx"
    df2.to_excel(image_file_path,index=False)

    cursor.close()
    connection.close()
    return df,df2,site,check_path


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
    db = download_whole_dynamodb_table.download_table("DFU_Master_ImageCollections")
    db = db[db["StudyName"] == "DFU_SSP"]


    site_loc = {
        "nynw":"/Volumes/dfu/DataTransfers/nynw/DFU_SS/NYNW_DFU_SMD2223-008_06_06_23(full)/SpectralView/dvsspdata.sql",
        "ocer":"/Volumes/dfu/DataTransfers/ocer/DFU_SS/OCER_DFU_SMD2148-019_06_08_23(full)/SpectralView/dvsspdata.sql",
        "whfa":"/Volumes/dfu/DataTransfers/whfa/DFU_SS/WHFA_DFU_SMD2223-007_04_11_23/SpectralView/dvsspdata.sql",
        "youngst":"/Volumes/dfu/DataTransfers/youngst/DFU_SS/YOUNGST_DFU_SMD2223-010_03_20_23/SpectralView/dvsspdata.sql",
        "lvrpool":"/Volumes/dfu/DataTransfers/lvrpool/DFU_SS/LVRPOOL_DFU_SMD2223-009-03_20_23/SpectralView/dvsspdata.sql",
        "hilloh":"/Volumes/dfu/DataTransfers/hilloh/DFU_SS/HILLOH_DFU_SMD2225-011_04_25_23/SpectralView/dvsspdata.sql",
        "grovoh":"/Volumes/dfu/DataTransfers/grovoh/DFU_SS/GROVOH_DFU_SMD2225-013_04_25_23/SpectralView/dvsspdata.sql",
        "mentoh":"/Volumes/dfu/DataTransfers/mentoh/DFU_SS/MENTOH_DFU_SMD2223-007_06_01_23/SpectralView/dvsspdata.sql",
        "encinogho":"/Volumes/dfu/DataTransfers/encinogho/DFU_SS/ENCINO_DFU_SMD2225-018_05_15_23/SpectralView/dvsspdata.sql",
        "lahdfu":"/Volumes/dfu/DataTransfers/lahdfu/DFU_SS/LASITE_DFU_SMD2225-019_06_01_23/SpectralView/dvsspdata.sql"
    }
    site_list=site_loc.keys()
    data_sites=[]
    for i in site_list:
        path = site_loc[i]
        df_guid, df_image, site, check_path = server_table_output(path)
        site_image = image_check(db, df_guid, df_image, site, check_path)
        data_sites.append(df_guid)

        if i =="whfa":
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: "203-"+x)
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: x.replace("-203", "-005") if "-203" in x else x)
        if i =="lvrpool":
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: x.replace("105","205") if "105" in x else x)
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: x.replace("205", "205-") if "205" in x else x)
        if i =="encinogho":
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: "210-"+x if "210" not in x else x)
        if i =="ocer":
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: "202-"+x if "202" not in x else x)
        if i =="youngst":
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: x.replace("204","204-") if "204" in x else x)
            df_guid["MedicalNumber"] = df_guid["MedicalNumber"].apply(lambda x: "204-"+x if "204-" not in x else x)


    union_df = pd.concat(data_sites)
    union_df.to_excel("/Users/ziweishi/Desktop/dfu_check.xlsx")



