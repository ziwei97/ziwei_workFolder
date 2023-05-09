import boto3
import os
import pandas as pd
import random
import pathlib

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

#replace table name based on request
table_name = 'BURN_Master_ImageCollections'
table = dynamodb.Table(table_name)

#get attributes from dynamodb
def get_attribute(table,guid,attr):

    response = table.get_item(
        Key={
            'ImgCollGUID': guid
        }
    )
    # print(response)
    return response["Item"][attr]


def download_raw(table,raw_list,attrs):
    fold = os.path.join("/Users/ziweishi/Documents", "phase3_msi")
    os.makedirs(fold)
    for i in raw_list:
        name = get_attribute(table,i,"Bucket")
        folder = os.path.join(fold, i)
        os.makedirs(folder)
        for j in attrs:
            try:
                attr = get_attribute(table,i,j)
                # pathlib.Path(path).parent.mkdir(exist_ok=True, parents=True)
                path = os.path.join(folder, j)
                os.makedirs(path)
                for s in attr:
                    file_name = s.split('/')[-1]
                    file_path = os.path.join(path, file_name)
                    # s3.meta.client.download_file(name, attr[0], str(path))
                    s3.Bucket(name).download_file(str(s), str(file_path))
            except Exception as e:
                print(e.args)






# data = pd.read_excel("/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.xlsx")
# df1 = data[data["Status"]=="acquired"]
# df1 = df1[df1["Tags"].isna()]
# df1 = df1[df1["Raw"].notna()]
# df1 = df1[[x[2:5]=="Raw" for x in df1['Raw']]]
# print(len(df1))


list_df = pd.read_excel("/Users/ziweishi/Desktop/final_list.xlsx")
list = list_df["guid"].to_list()

# df = df1[[x not in list for x in df1['ImgCollGUID']]]
#
# print(len(df))
#
# selected_list =df["ImgCollGUID"].to_list()
#
# guid_list = random.sample(selected_list,1500)
#
# df = df[df["ImgCollGUID"].isin(guid_list)]
#
# df = df[["ImgCollGUID","Raw","Site","SubjectID","StudyName"]]
#
# df.to_excel("/Users/ziweishi/Desktop/sample.xlsx")

attrs = ["Raw","Assessing"]

download_raw(table,list,attrs)