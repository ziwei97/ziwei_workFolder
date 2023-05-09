import boto3
import pandas as pd
import os
import download_request as download
import download_whole_dynamodb_table
import shutil
import color_drawing



s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')



#part 1: S3 bucket dataset num check step


def list_s3(bucket_name,prefix_name) ->list :
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    s3_address = []
    for object_summary in bucket.objects.filter(Prefix=prefix_name):
        key = object_summary.key
        if key != ".DS_Store":
            s3_address.append(key)
    return s3_address

def structure_initial(type_num):
    # prompt = """Choose File Structure: \n1. SubjectID/SV/GUID/File \n2. SubjectID/GUID/File \n3. SubjectID/Wound/GUID/File \n4. GUID/File\nYour Choice: """
    # choice = input(prompt)
    list_stru = ["SubjectID/SV/ImgCollGUID/file","SubjectID/ImgCollGUID/file","SubjectID/Wound/ImgCollGUID/file","ImgCollGUID/file"]
    structure= list_stru[int(type_num)-1]
    structure = structure.split("/")
    type_list = {i:[] for i in structure}
    return type_list,structure

def dataset_list_file(bucket_name,prefix_name):
    s3_list = list_s3(bucket_name,prefix_name)

    mode = 0
    sample = s3_list[2]
    sample = sample.replace(prefix_name,"")
    sample_list = sample.split("/")
    if "SV" in sample:
        mode = "1"
    elif len(sample_list) ==6:
        mode = "3"
    elif len(sample_list) == 5:
        mode = "2"
    else:
        mode = "4"
    data_structure = structure_initial(mode)
    structure_list = data_structure[0]
    column = data_structure[1]
    for i in s3_list:
        if ".DS_Store" not in i:

            key_list = i.split("/")
            if mode == "1":
                structure_list["SubjectID"].append(key_list[-4])
                structure_list["SV"].append(key_list[-3])
                structure_list["ImgCollGUID"].append(key_list[-2])
                structure_list["file"].append(key_list[-1])
            if mode == "2":
                structure_list["SubjectID"].append(key_list[-3])
                structure_list["ImgCollGUID"].append(key_list[-2])
                structure_list["file"].append(key_list[-1])
            if mode == "3":
                structure_list["SubjectID"].append(key_list[-4])
                structure_list["Wound"].append(key_list[-3])
                structure_list["ImgCollGUID"].append(key_list[-2])
                structure_list["file"].append(key_list[-1])
            if mode == "4":
                structure_list["ImgCollGUID"].append(key_list[-2])
                structure_list["file"].append(key_list[-1])


    df = pd.DataFrame(structure_list, columns=column)
    df.to_excel("/Users/ziweishi/Desktop/file_check.xlsx")



def num_check():
    df = pd.read_excel("/Users/ziweishi/Desktop/file_check.xlsx")
    column = list(df.columns)
    column.remove("file")
    column = column[1:]
    print(column)
    guid_list = df["ImgCollGUID"].to_list()
    guid = []
    for i in guid_list:
        if i not in guid:
            guid.append(i)
    type_list = {}
    attrs = ["Assessing","Raw","PseudoColor","Mask","FinalTruth"]
    final_column = column + attrs

    for k in final_column:
        type_list[k] = []

    for i in guid:
        df_sub = df[df["ImgCollGUID"] == i]
        for u in column:
            type_list[u].append(df_sub[u].iloc[0])
        file_sub = df_sub["file"].to_list()
        num_initial = {p: 0 for p in attrs}

        for j in file_sub:
            if j[0:4] == "Raw_" or j[0:4] == "MSI_":
                num_initial["Raw"] += 1
            if j[0:9] == "Assessing":
                num_initial["Assessing"] += 1
            if "PseudoColor" in j and ".tif" in j:
                num_initial["PseudoColor"] += 1
                if j[-1] != "f":
                    print(i)
            if j[0:4] == "Mask":
                num_initial["Mask"] += 1
            if "Truth_" in j and ".png" in  j:
                num_initial["FinalTruth"] += 1

        for x in attrs:
            type_list[x].append(num_initial[x])

    df_final = pd.DataFrame(type_list, columns=final_column)
    df_final.to_excel("/Users/ziweishi/Desktop/num_check.xlsx")
    print("finish check")

def file_num_check(bucket_name, prefix_name):
    dataset_list_file(bucket_name,prefix_name)
    num_check()



bucket_name = "spectralmd-datashare"
prefix_name = "DataScience/ePOC_All_Data_Request_2023-05-04/"
file_num_check(bucket_name,prefix_name)



#Part 2: S3 bucket dataset Image Quality Check

def download_image_check(bucket_name,prefix_name):
    s3 = boto3.resource('s3')
    list = list_s3(bucket_name,prefix_name)
    guid_list=[]
    file_list=[]
    for i in list:
        key_list = i.split("/")
        file = key_list[-1]
        guid = key_list[-2]
        if ".png" in file or file[0:4]=="Pseu":
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
        print(index+"/"+len(guid_list))


#Part 3: Change Wrong Final Truth color and replace them in S3 data set and S3 database.
def replace_reupload_truth(folder_path,guid,prefix):
    table = dynamodb.Table("BURN_Master_ImageCollections")
    final_turth1 = download.get_attribute(table,guid,"FinalTruth")
    final_turth = ', '.join(final_turth1)
    file_name = final_turth.split("/")[-1]
    print(file_name)
    bucket = download.get_attribute(table,guid,"Bucket")

    local_guid_path = os.path.join(folder_path,guid)
    local_file_path = os.path.join(local_guid_path,file_name)
    print(local_file_path)
    color_drawing.color_convert(local_file_path,local_file_path)
    s3.Bucket(bucket).upload_file(local_file_path, final_turth)
    subject = download.get_attribute(table,guid,"SubjectID")
    wound = str(download.get_attribute(table,guid,"Wound"))
    s3_path = prefix+subject+"/"+wound+"/"+guid+"/"+file_name
    s3.Bucket("spectralmd-datashare").upload_file(local_file_path, s3_path)
