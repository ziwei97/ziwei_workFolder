import boto3
import pandas as pd
import os
from  botocore.client import Config
import boto3.s3.transfer as s3transfer
import shutil
import util.update_attr as update
import check_data



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
    table_name = 'DFU_Master_ImageCollections'
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
                        a_source_pseduo = prefix+i+"/"  + a
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



def data_prepare_simple(guid,attrs,local):
    if os.path.isdir(local) == True:
        shutil.rmtree(local)
        os.mkdir(local)
    else:
        os.mkdir(local)
    s3_client = boto3.client("s3", config=Config(max_pool_connections=50))
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=20,
    )
    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)
    index = 0
    issue = []
    try:
        for i in guid:
            print(index)
            print(guid)
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
                        a1 = a.split("/")[-1]
                        a_source_pseduo = prefix+i+"/"  + a
                        dest_source = {
                            'Bucket': 'spectralmd-datashare',
                            'Key': a_source_pseduo
                        }
                        # s3t.copy(copy_source=copy_source, bucket=dest_source["Bucket"], key=dest_source["Key"])

                        local_path = local + a1
                        print(local_path)
                        s3t.download(bucket, a,local_path)
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
        # print(index)
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
def mask_download(df_file_check,folder):
    if os.path.isdir(folder) == True:
        shutil.rmtree(folder)
        os.mkdir(folder)
    else:
        os.mkdir(folder)
    guid = df_file_check["ImgCollGUID"].to_list()
    assess = df_file_check["Assessing"].to_list()
    pseudo = df_file_check["PseudoColor"].to_list()
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


def delete_archived(df,df_file):
    df_archived = df[df["phase"]=="archived"]
    ar_list = df_archived["ImgCollGUID"].to_list()
    print(len(ar_list))
    for i in ar_list:
        file_path = df_file[df_file["ImgCollGUID"]==i]
        try:
            ass_file = file_path["Assessing"].iloc[0]
            s3_object = s3.Object('spectralmd-datashare',ass_file)
            s3_object.delete()
        except:
            print("no assessing")
        try:
            pseudo_file = file_path["PseudoColor"].iloc[0]
            s3_object = s3.Object('spectralmd-datashare', pseudo_file)
            s3_object.delete()
        except:
            print("no pseudo")


def update_guid_phase(table,df,value):
    guid = df["ImgCollGUID"].to_list()
    phase = df["phase"].to_list()
    index = 0
    for i in guid:
        p = phase[index]
        if p == "archived":
            update.update_guid(table,i,"phase","archived")
        else:
            update.update_guid(table, i, "phase", value)


# def prepare_flow(df,folder,attrs,prefix,bucket):
#     mask_prepare(df,attrs,prefix)
#     df_file = check_data.mask_check(bucket,prefix)
#     mask_download(df_file,folder)
#     return df_file
#
#
# def update_flow(df,df_file,table,value):
#     delete_archived(df,df_file)
#     update_guid_phase(table,df,value)




if __name__ == "__main__":
    table_name = 'DFU_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    folder_path = "/Users/ziweishi/Documents/check/"
    bucket = "spectralmd-datashare"
    attrs=["PseudoColor","Raw"]
    prefix="DataScience/DFU_Measurement_test/"

    df = pd.read_excel("/Users/ziweishi/Desktop/3D_Measurement_test_Sample.xlsx")

    # print(len(df))
    # data_prepare(df,attrs,prefix)


    # check_data.file_num_check(bucket,prefix)














    print("aws s3 cp s3://spectralmd-datashare/"+prefix+ " /Users/ziweishi/Documents/DFU_Measurement_test/  --recursive")
    # print("aws s3 cp s3://spectralmd-datashare/"+prefix+ " /your/target  --recursive")

































