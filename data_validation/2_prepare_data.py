import boto3
import pandas as pd
import os
from  botocore.client import Config
import boto3.s3.transfer as s3transfer
import util.update_attr as update

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def get_attribute(table, guid, attr):
    response = table.get_item(
        Key={
            'ImgCollGUID': guid
        }
    )
    return response["Item"][attr]

# general data prepare, revise data_structure first
def data_prepare(df,attrs,prefix):
    s3_client = boto3.client("s3", config=Config(max_pool_connections=50))
    table_name = 'BURN_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )
    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)
    index = 0
    issue = []
    guid = df["ImgCollGUID"].to_list()
    sub = df["SubjectID"].to_list()
    # wound = df["Wound"].to_list()
    # sv = df["VisitTime"].to_list()
    mask_index = 0
    try:
        for i in guid:
            print(index)
            subject = sub[index]
            # wo = wound[index]
            # sv_n = sv[index]
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
                        a = a.split("/")[-1]
                        a_source_pseduo = prefix+subject+"/"+i+"/"  + a
                        dest_source = {
                            'Bucket': 'spectralmd-datashare',
                            'Key': a_source_pseduo
                        }
                        s3t.copy(copy_source=copy_source, bucket=dest_source["Bucket"], key=dest_source["Key"])
                except:
                    print(i+" no "+j)
    except Exception as err:
        issue.append(err)
    finally:
        s3t.shutdown()


# specific structure for LYD company
def mask_prepare(df,attrs,prefix):
    s3_client = boto3.client("s3", config=Config(max_pool_connections=50))
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )
    index = 0
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
                        dest_source = {
                            'Bucket': 'spectralmd-datashare',
                            'Key': a_source_pseduo
                        }
                        s3t.copy(copy_source=copy_source, bucket=dest_source["Bucket"], key=dest_source["Key"])
                    elif j == "PseudoColor":
                        a_source_pseduo = prefix + "PseudoColor/PseudoColor_" + i + ".tif"
                        dest_source = {
                            'Bucket': 'spectralmd-datashare',
                            'Key': a_source_pseduo
                        }
                        s3t.copy(copy_source=copy_source, bucket=dest_source["Bucket"], key=dest_source["Key"])
                    else:
                        print("no attributes")
            except:
                print(i + " missing " + j)
    s3t.shutdown()


# download to check image quality
def mask_download(df,folder):
    os.mkdir(folder)
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
                file_name = "fake_" + file_name
                file_path = os.path.join(guid_path, file_name)
                s3t.download(bucket, pseudo_key, file_path)
        index+=1
        print(index)
    s3t.shutdown()
    print("done")



if __name__ == "__main__":
    attrs=["PseudoColor","Assessing"]
    prefix="DataScience/WAUSI_Phase4_PseudoAssess_0830/"
    # path = "/Users/ziweishi/Documents/DFU_regular_update/20230830tra_1/20230830tra_1_download_list.xlsx"
    # df = pd.read_excel(path)
    # # data_prepare(df,attrs,prefix)
    # mask_prepare(df,attrs,prefix)



    path ="/Users/ziweishi/Desktop/file_check.xlsx"
    df = pd.read_excel(path)
    mask_download(df,"/Users/ziweishi/Documents/check1/")
















