import boto3
import pandas as pd
import os
import download_request as download
import download_whole_dynamodb_table
import shutil

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')




def get_attribute(table,guid,attr):
    response = table.get_item(
        Key={
            'ImgCollGUID': guid
        }
    )
    return response["Item"][attr]


#change test


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

    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)

    # db = download_whole_dynamodb_table.download_table('DFU_Master_ImageCollections')

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
    sub = df["SubjectID"].to_list()
    # vis = df["VisitTime"].to_list()

    issue = []


    index = 0
    for i in guid:
        subject = sub[index]
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
                    a_source_pseduo = prefix + subject + "/"+ i + "/" + a
                    s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)

            except:
                issue.append(i + " " + j + " " + "Missing")
        index += 1
        print(index)
    print(issue)



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




# path = "/Users/ziweishi/Desktop/epoc_summary.xlsx"
prefix="DataScience/ePOC_All_Data_Request_2023-05-04/"
# epoc_data_prepare(path,["Raw","Assessing"],prefix)

list1 = """3a6edceb-13cb-4c5b-bb8f-b300ad81d422
6f12db9a-16b6-493d-8683-0c0092b75dc2
91a29a28-2871-4cc4-9fd3-2b96163686d2
afc131e1-992e-43d5-8bbe-98c4af7337a3"""

guid = list1.split("\n")
attrs=["Mask"]

table_name = 'BURN_Master_ImageCollections'
table = dynamodb.Table(table_name)
index=0
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
            print(str(index) + " " + i + " " + j)
    index += 1


