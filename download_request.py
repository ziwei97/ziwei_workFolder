import boto3
import os
import numpy as np
import pandas as pd
import random
import pathlib
import cv2

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')



#get attributes from dynamodb
def get_attribute(table,guid,attr):
    try:
        response = table.get_item(
            Key={
                'ImgCollGUID': guid
            }
        )
        # print(response)
        return response["Item"][attr]
    except:
        return  np.nan


def download_raw(table,raw_list,attrs,path):
    index=1
    error_list=[]
    fold = path
    # if os.path.isdir(fold) == True:
    #     os.remove(fold)
    os.makedirs(fold)
    # id_list=[]
    # size_list=[]
    # mask_list=[]
    for i in raw_list:
        print(index)
        name = get_attribute(table,i,"Bucket")
        # subject = get_attribute(table, i, "SubjectID")
        # wound = get_attribute(table, i, "Wound")
        # sub_folder = os.path.join(fold,subject)
        guid_folder = os.path.join(fold,i)
        if os.path.isdir(guid_folder) == False:
            os.mkdir(guid_folder)

        # wound_folder = os.path.join(sub_folder,wound)
        # if os.path.isdir(wound_folder) == False:
        #     os.mkdir(wound_folder)

        # guid_folder = os.path.join(wound_folder,i)
        # os.mkdir(guid_folder)

        for j in attrs:
            try:
                if j=="PseudoColor":
                    s = "PseudoColor/PseudoColor_" + str(i) + ".tif"
                    file_name = "PseudoColor_" + str(i) + ".tif"
                    file_path = os.path.join(guid_folder, file_name)
                    s3.Bucket(name).download_file(s, str(file_path))

                # if j=="PrimaryDoctorTruth":
                #     attr = get_attribute(table, i, j)
                #     for s in attr:
                #         file_name = s.split('/')[-1]
                #         file_name1 = "Primary_" + file_name
                #         file_path = os.path.join(guid_folder, file_name1)
                #         s3.Bucket(name).download_file(s, str(file_path))
                #
                # if j=="SecondaryDoctorTruth":
                #     attr = get_attribute(table, i, j)
                #     for s in attr:
                #         file_name = s.split('/')[-1]
                #         file_name1 = "Secondary_" + file_name
                #         file_path = os.path.join(guid_folder, file_name1)
                #         s3.Bucket(name).download_file(s, str(file_path))

                else:
                    attr = get_attribute(table, i, j)
                    for s in attr:
                        file_name = s.split('/')[-1]

                        file_path = os.path.join(guid_folder, file_name)
                        s3.Bucket(name).download_file(str(s), str(file_path))
                        # img = cv2.imread(file_path)
                        # sp = img.shape
                        # id_list.append(i)
                        # size_list.append(sp)
                        # mask_list.append(file_name)
                        # print(sp)
            except:
                error_list.append(i)
                print(i)
        index+=1

    # data = zip(id_list,mask_list,size_list)
    # final = pd.DataFrame(data,columns=["GUID","Mask","Size"])
    # final.to_excel("/Users/ziweishi/Desktop/epoc_mask_size.xlsx")



def replace_all(text,reo):
    for i in reo:
        if i in text:
            text.replace("i","")
    return text


if __name__ == "__main__":


    # path = "/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.xlsx"
    # df = pd.read_excel(path)
    # sub_list=["105-016","105-018","105-024","105-031"]
    #
    # df = df[df["SubjectID"].isin(sub_list)]
    # df = df[["ImgCollGUID", "Wound", "SubjectID", "Status","Tags","PseudoColor","PrimaryDoctorTruth","SecondaryDoctorTruth"]]
    #
    # final = pd.DataFrame(columns=["ImgCollGUID", "Wound", "SubjectID", "Status","Tags","PseudoColor","PrimaryDoctorTruth","SecondaryDoctorTruth"])
    # wound_list=[[1,2,3,4],[3],[1],[1]]
    #
    #
    # index=0
    # for i in sub_list:
    #     df_sub=df[df["SubjectID"]==i]
    #     df_sub1 = df_sub[df_sub["Wound"].isin(wound_list[index])]
    #     final = pd.concat([final,df_sub1],axis=0)
    #     index+=1
    #
    #
    # final = final[final["Status"]=="acquired"]
    # final.to_excel("/Users/ziweishi/Documents/doctor_truth.xlsx")

    raw_list ="19f80dc3-0a82-4554-8cc8-81e370103024"
    raw_list = raw_list.split("\n")
    attrs = ["Mask"]

    table_name = 'BURN_Master_ImageCollections'
    table = dynamodb.Table(table_name)
    download_raw(table, raw_list, attrs, "/Users/ziweishi/Documents/MASK_convert")








