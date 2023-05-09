import os
import pandas as pd
import download_whole_dynamodb_table
import download_request
import boto3

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

bucket_list_cor = """whfa
nynw
ocer
lvrpool
grovoh
hilloh
mentoh
youngst"""

bucket_list = bucket_list_cor.split("\n")



def replace_all(site,patient_id):
    if site == "whfa":
        list = []
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")

        if "_203" in patient_id:
            patient_id=patient_id.replace("_203","_005")

        patient_id=patient_id.replace("Patient_","203-")

    if site == "grovoh":
        list = ["_208-"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_","208-")

    if site == "hilloh":
        list = ["_207-"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_","207-")

    if site == "lvrpool":
        list = ["_105","_205"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_","205-")

    if site == "mentoh":
        list = ["_209-"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_","209-")

    if site == "nynw":
        list = ["_201-"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")

        if "999-001" in patient_id:
            patient_id=patient_id.replace("999-001","test")

        patient_id=patient_id.replace("Patient_","201-")

    if site == "ocer":
        list = ["_202-"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_","202-")

    if site == "youngst":
        list = ["_204"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")

        if "000-999" in patient_id:
            patient_id=patient_id.replace("000-999","test")
        patient_id=patient_id.replace("Patient_","204-")




    return patient_id


def server_file_refresh():
    site = []
    device = []
    patient_list = []
    location_list = []
    file_list = []

    SubjectID = []

    test_suffix = ["0000", "9999", "999-001", "000-999", "test"]

    for i in bucket_list:
        path = "/Volumes/dfu/DataTransfers/"
        folder_path = os.path.join(path, i)
        DFU_path = os.path.join(folder_path, "DFU_SSP")
        device_id_list = os.listdir(DFU_path)
        for j in device_id_list:
            if j[0:3] == 'SMD':
                device_path = os.path.join(DFU_path, j)
                patient_path = os.path.join(device_path, "SpectralView/Diabetic_Foot_Ulcer")
                patients = os.listdir(patient_path)
                for p in patients:
                    if p[0] != ".":
                        patient_id = replace_all(i, p)
                        patient_suffix = patient_id.split("-")[-1]
                        if patient_suffix not in test_suffix:
                            location_path = os.path.join(patient_path, p)
                            locations = os.listdir(location_path)
                            for q in locations:
                                if q[0] != ".":
                                    img_path = os.path.join(location_path, q)
                                    images = os.listdir(img_path)
                                    for x in images:
                                        if x[0:5] == "Image" and x[-3:] != "zip":
                                            file_list.append(x)
                                            location_list.append(q)
                                            patient_list.append(patient_id)
                                            device.append(j)
                                            site.append(i)

    data = zip(site, device, patient_list, location_list, file_list)
    server_final = pd.DataFrame(data, columns=["Site", "Device", "SubjectID", "AnatomicalLocation", "Collection_file"])
    server_final.to_excel("/Users/ziweishi/Documents/DFU_Server_Check/Step1_Server_summary.xlsx")
    return server_final


def db_check_compare():
    server_final = pd.read_excel("/Users/ziweishi/Documents/DFU_Server_Check/Step1_Server_summary.xlsx")

    sub_list = server_final["SubjectID"].to_list()
    SubjectID = []

    for i in sub_list:
        if i not in SubjectID:
            SubjectID.append(i)

    df = download_whole_dynamodb_table.download_table('DFU_Master_ImageCollections')
    column = ["ImgCollGUID", "SubjectID", "AnatomicalLocation", "Tags", "Status", "Site", "StudyName", "Bucket",
              "PseudoColor"]
    df = df.loc[:, column]
    df = df[df["StudyName"] == "DFU_SSP"]
    df = df[df["SubjectID"].isin(SubjectID)]
    df = df[df["PseudoColor"].notna()]
    df.to_excel('/Users/ziweishi/Documents/DFU_Server_Check/Step2_db_summary.xlsx')

    miss_sub = []
    server_num = []
    db_num = []
    for i in SubjectID:
        server_subset = server_final[server_final["SubjectID"] == i]
        db_subset = df[df["SubjectID"] == i]
        a = len(server_subset)
        b = len(db_subset)
        if a != b:
            miss_sub.append(i)
            server_num.append(a)
            db_num.append(b)
            print(i + " Server: " + str(a) + " DB: " + str(b))

    data = zip(miss_sub, server_num, db_num)

    df_compare = pd.DataFrame(data, columns=["SubjectID", "Server_Num", "DB_Num"])
    df_compare.to_excel('/Users/ziweishi/Documents/DFU_Server_Check/Step3_compare_summary.xlsx')

    issue_db_subset = df[df["SubjectID"].isin(miss_sub)]
    issue_db_subset = issue_db_subset[["SubjectID", "AnatomicalLocation", "ImgCollGUID", "Bucket"]]
    issue_db_subset.to_excel('/Users/ziweishi/Documents/DFU_Server_Check/Step4_issue_db.xlsx')
    issue_server_subset = server_final[server_final["SubjectID"].isin(miss_sub)]
    issue_server_subset.to_excel('/Users/ziweishi/Documents/DFU_Server_Check/Step4_issue_server.xlsx')





def down_issue(subjectid):
    issue_db = pd.read_excel('/Users/ziweishi/Documents/DFU_Server_Check/Step4_issue_db.xlsx')
    issue_server = pd.read_excel('/Users/ziweishi/Documents/DFU_Server_Check/Step4_issue_server.xlsx')

    df_guid_list = issue_db[issue_db["SubjectID"]==subjectid]
    guid = df_guid_list["ImgCollGUID"].to_list()

    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    attrs=["PseudoColor"]
    path = os.path.join("/Users/ziweishi/Documents/DFU_Server_Check/",subjectid)
    download_request.download_raw(table,guid,attrs,path)



db_check_compare()