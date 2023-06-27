import boto3
import pandas as pd
import os
import download_request as download
import download_whole_dynamodb_table
import shutil
import test_copy
import threading
from  botocore.client import Config
from boto3.s3.transfer import TransferConfig
import boto3.s3.transfer as s3transfer

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# table_name = 'BURN_Master_ImageCollections'
# table = dynamodb.Table(table_name)


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
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    df = pd.read_excel(excel_path)
    df = df[df["Sequence"]==0]
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
            if j=="PseudoColor":
                try:
                    label = get_attribute(table, i, j)
                    for a in label:
                        a_source = a
                        copy_source = {
                            'Bucket': bucket,
                            'Key': a_source
                        }
                        a = a.split("/")[-1]
                        a_source_pseduo = prefix + subject + "/" + "SV" + str(
                            visit_time) + "/" + i + "/" + a
                        dest_source={
                            'Bucket': 'spectralmd-datashare',
                            'Key': a_source_pseduo
                        }
                        if "PseudoColor.tif" in a:
                            test_copy.s3_copy(copy_source, dest_source)
                            # s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
                except:
                    issue.append(i + " " + j + " " + "Missing")
                    print(i + " " + j + " " + "Missing")
            else:
                try:
                    label = get_attribute(table, i, j)
                    for a in label:
                        a_source = a
                        copy_source = {
                            'Bucket': bucket,
                            'Key': a_source
                        }
                        a = a.split("/")[-1]
                        a_source_pseduo = prefix + subject + "/" + "SV" + str(
                            visit_time) + "/" + i + "/" + a
                        dest_source = {
                            'Bucket': 'spectralmd-datashare',
                            'Key': a_source_pseduo
                        }
                        test_copy.s3_copy(copy_source, dest_source)
                        # s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
                except:
                    issue.append(i + " " + j + " " + "Missing")
                    print(i + " " + j + " " + "Missing")
        index += 1
        print(index)
    print(issue)

def wausi_data_prepare(df,attrs,prefix):
    s3_client = boto3.client("s3", config=Config(max_pool_connections=50))
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )
    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)
    issue = []
    index = 0
    guid = df["ImgCollGUID"].to_list()
    sub = df["SubjectID"].to_list()
    sv = df["VisitTime"].to_list()
    try:
        for i in guid:
            print(index)
            subject = sub[index]
            sv_n = sv[index]
            bucket = get_attribute(table, i, "Bucket")
            index += 1
            for j in attrs:
                label = get_attribute(table, i, j)
                for a in label:
                    a_source = a
                    copy_source = {
                        'Bucket': bucket,
                        'Key': a_source
                    }
                    a = a.split("/")[-1]
                    a_source_pseduo = prefix + subject + "/" + i + "/" + a
                    dest_source = {
                        'Bucket': 'spectralmd-datashare',
                        'Key': a_source_pseduo
                    }
                    s3t.copy(copy_source=copy_source, bucket=dest_source["Bucket"],key = dest_source["Key"])
    except Exception as err:
        issue.append(i + " " + j + " " + "Missing")
        print(err)

    finally:
        s3t.shutdown()




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
                    dest_source = {
                        'Bucket': 'spectralmd-datashare',
                        'Key': a_source_pseduo
                    }
                    test_copy.s3_copy(copy_source, dest_source)
                    # s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)

            except:
                # issue.append(i + " " + j + " " + "Missing")
                print(str(index)+" "+i+" "+j)
        index += 1
        print(index)
    # print(issue)

# def simple_data_prepare(corpus,attrs,prefix):
#     guid = corpus.split("\n")
#     index = 0
#     for i in guid:
#         print(i)
#         bucket = get_attribute(table, i, "Bucket")
#         for j in attrs:
#             try:
#                 label = get_attribute(table, i, j)
#                 for a in label:
#                     a_source = a
#                     copy_source = {
#                         'Bucket': bucket,
#                         'Key': a_source
#                     }
#                     a = a.split("/")[-1]
#                     a_source_pseduo = prefix+ i + "/" + a
#                     dest_source = {
#                         'Bucket': 'spectralmd-datashare',
#                         'Key': a_source_pseduo
#                     }
#                     test_copy.s3_copy(copy_source,dest_source)
#                     # s3.meta.client.copy(copy_source, 'spectralmd-datashare', a_source_pseduo)
#             except:
#                 print(i)
#         index += 1
#         print(index)

def simple_data_upload(corpus,folder,prefix):
    guid = corpus.split("\n")
    index=0
    for i in guid:
        print(i)
        name = "Mask_"+i+".png"
        local_file_path = folder+name
        s3_file_path = prefix+"Mask_"+i+".png"
        # s3.Object('spectralmd-datashare', s3_file_path).delete()
        s3.Bucket("spectralmd-datashare").upload_file(local_file_path, s3_file_path)
        index+=1
        print(index)


# def folder_data_upload(df,guid,folder):
#     guid = df["GUID"].to_list()
#     index = 0
#     for i in guid:
#         name = "Mask_" + i + ".png"
#         local_file = folder + name
#         bucket = download.get_attribute(table, i, "Bucket")
#         try:
#             s3_file_path = "Mask/" + name
#             s3.Bucket(bucket).upload_file(local_file, s3_file_path)
#         except:
#             print(i)
#         print(bucket + " " + i)
#         index += 1


def mask_prepare(excel_path,attrs,prefix):
    s3_client = boto3.client("s3", config=Config(max_pool_connections=50))
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )

    issue = []
    index = 0

    df = pd.read_excel(excel_path)
    guid = df["ImgCollGUID"].to_list()

    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)

    for i in guid:
        print(index)
        bucket = get_attribute(table, i, "Bucket")
        index += 1
        for j in attrs:
            try:
                label = get_attribute(table, i, j)
                for a in label:
                    a_source = a
                    copy_source = {
                        'Bucket': bucket,
                        'Key': a_source
                    }
                    # a = a.split("/")[-1]
                    if j == "Assessing":
                        a_source_pseduo = prefix + "Assessing/Assessing_" + i + ".png"
                    elif j == "PseudoColor":
                        a_source_pseduo = prefix + "PseudoColor/PseudoColor_" + i + ".tif"
                    else:
                        print("no attributes")

                    dest_source = {
                        'Bucket': 'spectralmd-datashare',
                        'Key': a_source_pseduo
                    }
                    s3t.copy(copy_source=copy_source, bucket=dest_source["Bucket"], key=dest_source["Key"])
            except:
                print(i + " missing " + j)



    s3t.shutdown()

def mask_download(excel_path,folder):
    os.mkdir(folder)
    df = pd.read_excel(excel_path)
    guid = df["ImgCollGUID"].to_list()
    assess = df["Assessing"].to_list()
    pseudo = df["PseudoColor"].to_list()
    s3_client = boto3.client("s3", config=Config(max_pool_connections=50))
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )

    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)
    index=0
    for i in guid:
        bucket = "spectralmd-datashare"
        assess_key=assess[index]
        pseudo_key=pseudo[index]
        download_list = []
        download_list.append(assess_key)
        download_list.append(pseudo_key)

        guid_path = folder + i
        os.mkdir(guid_path)
        for j in download_list:
            try:
                file_name = j.split("/")[-1]
                file_path = os.path.join(guid_path, file_name)
                s3t.download(bucket, j, file_path)
            except:
                file_name = pseudo_key.split("/")[-1]
                file_name = "fake_"+file_name
                file_path = os.path.join(guid_path, file_name)
                s3t.download(bucket, pseudo_key, file_path)

        index+=1
        print(index)

    s3t.shutdown()
    print("done")

if __name__ == "__main__":
    attrs=["PseudoColor"]
    prefix="DataScience/GroundTruth_Pseudo_0620/"

    subject=""""""

    subject_list = subject.split("\n")

    df = pd.read_excel("/Users/ziweishi/Documents/DFU_regular_update/20230620/20230620_Guid_list.xlsx")

    df = df[df["SubjectID"].isin(subject_list)]

    wausi_data_prepare(df,attrs,prefix)



