import boto3
import numpy as np
import pandas as pd
import os
import download_request as download
import download_whole_dynamodb_table
import shutil

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def list_s3(bucket_name,prefix_name) ->list :
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    prefix = prefix_name
    s3_address = []
    for object_summary in bucket.objects.filter(Prefix=prefix):
        key = object_summary.key
        s3_address.append(key)

    return s3_address

# check s3 prepared package for ds team
def num_check(bucket_name,prefix_name):
    s3_list = list_s3(bucket_name,prefix_name)
    guid_list = []
    file_list = []
    for i in s3_list:
        key_list = i.split("/")
        guid_list.append(key_list[-2])
        file_list.append(key_list[-1])
    data = zip(guid_list, file_list)
    df = pd.DataFrame(data, columns=["ImgCollGUID", "file"])
    guid = []
    for i in guid_list:
        if i not in guid:
            guid.append(i)
    raw_num=[]
    pseudo_num = []
    assessing_num=[]
    mask_num=[]
    for i in guid:
        df_sub = df[df["ImgCollGUID"]==i]
        file_sub = df_sub["file"].to_list()
        raw = 0
        pse = 0
        ass = 0
        mask = 0
        for j in file_sub:
            if j[0:4]=="Raw_":
                raw+=1
            if j[0:9]=="Assessing":
                ass+=1
            if j [0:11]=="PseudoColor":
                pse+=1
            if j[0:4]=="Mask":
                mask+=1
        raw_num.append(raw)
        assessing_num.append(ass)
        pseudo_num.append(pse)
        mask_num.append(mask)

    df_total = zip(guid,raw_num,assessing_num,pseudo_num,mask_num)
    df_final = pd.DataFrame(df_total,columns=["ImgCollGUID","Raw_num","Assessing_num","PseudoColor_num","Mask_num"])
    df_final.to_excel("/Users/ziweishi/Desktop/num_check.xlsx")
    print("finish check")

def download_image_check(bucket_name,prefix_name):
    s3 = boto3.resource('s3')
    list = list_s3(bucket_name,prefix_name)
    guid_list=[]
    file_list=[]
    for i in list:
        key_list = i.split("/")
        file = key_list[-1]
        guid = key_list[-2]
        if file[0:4] == "Mask" or file[0:4] == "Pseu":
            file_list.append(i)
            guid_list.append(guid)
    index = 0
    path = "/Users/ziweishi/Desktop/data_check"
    os.mkdir(path)
    for i in file_list:
        id = guid_list[index]
        guid_path = os.path.join(path,id)
        if os.path.isdir(guid_path) == False:
            os.mkdir(guid_path)
        file_name = (i.split("/"))[-1]
        file_path = os.path.join(guid_path,file_name)
        s3.Bucket(bucket_name).download_file(i, file_path)
        index+=1
        print(index)






# 2. check database in dynamodb

def final_truth_check(truth_file_path):
    table_name = 'BURN_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    df_truth = pd.read_excel(truth_file_path)
    list = df_truth["ImgCollGUID"].to_list()
    subjectid = df_truth["SubjectID"].to_list()
    wound = df_truth["Wound"].to_list()
    imgid = df_truth["ImageCollectionID"].to_list()

    finish = 0
    index = 0
    for i in list:
        try:
            final_truth = download.get_attribute(table, i, "FinalTruth")
            finish += 1

            # print(i + " " + subjectid[index] + " " + str(wound[index]) + " " + str(imgid[index]))

        except:
            print(i + " " + subjectid[index] + " " + str(wound[index]) + " " + str(imgid[index]))

            finish += 0
        index += 1
    print("Finished Num: " + str(finish) + " /" + str(len(list)))



def image_check_db(guid_path,attrs):
    table_name = 'BURN_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    attrs = ["PseudoColor", "FinalTruth"]

    df_truth = pd.read_excel(guid_path)
    list = df_truth["ImgCollGUID"].to_list()
    download.download_raw(table,list,attrs)


# 3. truthing work table_name: BURN_Master_ImageCollections

def truth_filter(file_name):
    df = download_whole_dynamodb_table.download_table("BURN_Master_ImageCollections")
    column = ["ImgCollGUID", "SubjectID", "ImageCollectionID", "AnatomicalLocation", "Suffix", "Wound",
              "PrimaryDoctorTruth", "SecondaryDoctorTruth", "FinalTruth", "Tags", "Status", "Site", "StudyName",
              "Bucket"]
    df3 = df.loc[:, column]
    df4 = df3[df3["StudyName"] == "BURN_BTS"]
    df5 = df4[df4["Status"] == "acquired"]
    df6 = df5[df5["FinalTruth"].isna()]
    df7 = df6[df6["Tags"].isna()].reset_index(drop=True)
    path = '/Users/ziweishi/Documents/Truthing/'
    file_path = os.path.join(path,file_name)
    df7.to_excel(file_path)
    return df7

#
# table_name = 'DFU_Master_ImageCollections'
# table = dynamodb.Table(table_name)
#
# dfu = download_whole_dynamodb_table.download_table(table_name)
#
# df = pd.read_excel("/Users/ziweishi/Desktop/num_check.xlsx")
#
# guid = df["ImgCollGUID"].to_list()
#
# status=[]
# tags=[]
#
# for i in guid:
#     df_set = dfu[dfu["ImgCollGUID"]==i]
#     sta = df_set["Status"].iloc[0]
#     tag = df_set["Tags"].iloc[0]
#     status.append(sta)
#     tags.append(tag)
#
# df["Status"]=status
# df["Tags"]=tags
#
#
# df.to_excel("/Users/ziweishi/Desktop/WAUSI_info.xlsx")