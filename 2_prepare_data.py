import boto3
import pandas as pd
import os
import download_request as download
import download_whole_dynamodb_table
import shutil
import test_copy

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

table_name = 'DFU_Master_ImageCollections'
table = dynamodb.Table(table_name)


def get_attribute(table,guid,attr):
    response = table.get_item(
        Key={
            'ImgCollGUID': guid
        }
    )
    return response["Item"][attr]

def return_attribute(table,guid,attr):
    table_set = table[table["ImgCollGUID"]==guid]
    if attr =="Bucket":
        value = table_set[attr].iloc[0]
    else:
        value = table_set[attr].iloc[0]
        value = value[1:-1]
        value = value.replace("'", "")
        value = value.replace(" ", "")
        value = value.split(",")
    return value

def wasp_data_prepare(excel_path,attrs,prefix):
    df = pd.read_excel(excel_path)
    guid = df["ImgCollGUID"].to_list()
    sub = df["SubjectID"].to_list()
    visit = df["Sequence"].to_list()
    issue = []
    index = 0
    for i in guid:
        subject = sub[index]
        visit_time = visit[index]
        bucket = get_attribute(table, i, "Bucket")
        for j in attrs:
            try:
                label = get_attribute(table, i, j)
                for a in label:
                    print(a)
                    a_source = a
                    copy_source = {
                        'Bucket': bucket,
                        'Key': a_source
                    }
                    a = a.split("/")[-1]
                    a_source_pseduo = prefix + subject + "/" + "SV" + str(
                        visit_time) + "/" + i + "/" + a
                    s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
            except:
                issue.append(i + " " + j + " " + "Missing")
        index += 1
        print(index)
    print(issue)

def wausi_data_prepare(excel_path,attrs,prefix):

    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    df = pd.read_excel(excel_path)
    guid = df["ImgCollGUID"].to_list()
    # sub = df["SubjectID"].to_list()
    # vis = df["VisitTime"].to_list()

    issue = []


    index = 0
    for i in guid:
        # subject = sub[index]
        # visit_time = vis[index]
        bucket = get_attribute(table, i, "Bucket")
        for j in attrs:

            try:
                label = get_attribute(table, i, j)

                for a in label:

                    a_source = a
                    copy_source = {
                        'Bucket': bucket,
                        'Key': a_source
                    }
                    a = a.split("/")[-1]
                    a_source_pseduo = prefix+ i + "/" + a
                    dest_source = {
                        'Bucket': 'spectralmd-datashare',
                        'Key': a_source_pseduo
                    }
                    test_copy.s3_copy(copy_source,dest_source)
                    # s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
            except:
                issue.append(i + " " + j + " " + "Missing")
        index += 1
        print(index)
    print(issue)
    data = pd.DataFrame(data=issue,columns=["issue"])
    data.to_excel("/Users/ziweishi/Documents/check.xlsx")

def epoc_data_prepare(excel_path,attrs,prefix):

    table_name = 'BURN_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    df = pd.read_excel(excel_path)
    guid = df["ImgCollGUID"].to_list()
    # sub = df["SubjectID"].to_list()


    issue = []


    index = 0
    for i in guid:
        # subject = sub[index]
        bucket = get_attribute(table, i, "Bucket")
        for j in attrs:
            try:
                label = get_attribute(table, i, j)
                for a in label:
                    a_source = a
                    copy_source = {
                        'Bucket': bucket,
                        'Key': a_source
                    }
                    a = a.split("/")[-1]
                    a_source_pseduo = prefix + i + "/" + a
                    s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
                print(index)
            except:
                # issue.append(i + " " + j + " " + "Missing")
                print(str(index)+" "+i+" "+j)
        index += 1

    # print(issue)

def simple_data_prepare(corpus,attrs,prefix):
    guid = corpus.split("\n")
    index = 0
    for i in guid:
        bucket = get_attribute(table, i, "Bucket")
        for j in attrs:
            try:
                label = get_attribute(table, i, j)
                for a in label:
                    a_source = a
                    copy_source = {
                        'Bucket': bucket,
                        'Key': a_source
                    }
                    a = a.split("/")[-1]
                    a_source_pseduo = prefix+ i + "/" + a
                    dest_source = {
                        'Bucket': 'spectralmd-datashare',
                        'Key': a_source_pseduo
                    }
                    # test_copy.s3_copy(copy_source,dest_source)
                    s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
            except:
                print(i)
        index += 1
        print(index)



attrs=["Raw","Mask"]
prefix="DataScience/WAUSI_PartI_0516/"

path="/Users/ziweishi/Documents/DFU_regular_update/20230516/20230516_Guid_list.xlsx"
wausi_data_prepare(path,attrs,prefix)









# cor="""7b3c0b74-14af-4363-8828-85b1e5756ad1
# e0973c9e-8022-43d5-8f07-5658300c6041
# 0b65fcf8-5a32-44f0-9e54-79487461a04f
# d77c33e7-f088-42e0-851a-a66863cb7339
# 5f7b3f3f-8551-489e-b48a-49fe70d64cf4"""

# simple_data_prepare(cor,attrs,prefix)
