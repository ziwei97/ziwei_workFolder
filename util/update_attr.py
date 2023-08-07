import boto3
import pandas as pd

dynamodb = boto3.resource('dynamodb')
table_name = 'DFU_Master_ImageCollections'  # 替换为你的 DynamoDB 表名
table = dynamodb.Table(table_name)


def update_guid(guid,attr,value):
    response = table.update_item(
        Key={
            'ImgCollGUID': guid,
        },
        UpdateExpression='SET #attr_name = :attr_value',
        ExpressionAttributeNames={
            '#attr_name': attr # 替换为你的新属性名
        },
        ExpressionAttributeValues={
            ':attr_value': value
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("success")
    else:
        print("fail")


if __name__ == "__main__":


    # df = pd.read_excel("/Users/ziweishi/Desktop/Book1.xlsx")
    # guid_list = df["ImgCollGUID"].to_list()
    # phase = df["phase"].to_list()
    # index=0
    # print(len(guid_list))
    # for i in guid_list:
    #     phase_num = phase[index]
    #     index+=1
    #     update_guid(i,"phase",phase_num)
    #     print(index)

    cor = """9ccc7fca-555f-4f51-b7b8-d6e7fcc6d032
3d26fb62-a7ad-4acc-a8c9-230a9040a6c9
9b7e33af-744e-43d4-9a0b-42240108cbb6
ba6bbc58-da27-4af3-a4cd-d381971b5823
d565e8ee-055f-43fd-a8a0-fa8576a4c4db
b408136a-16ee-4064-b051-f39ce4ae76ce
80d4da47-b2ac-467c-8750-c2e8f314bcd5
479f6fd5-6dca-4fe1-ab6d-3e555571ed26
208f8eef-b3df-4b7f-92ec-5ee8ee70d001
90ed0350-c025-4c5d-ab00-a868b8b0f9e8
64a982b5-b032-44e1-ba0c-6311db2aefa4
b023c543-b75e-46c5-9d10-3f5b6b1fa52a
0e658535-043d-4db4-ac1d-b9dd258329d0
a0408592-8fcc-4de6-b8a6-aae66635287f
025ebbef-fe56-4fcf-b6ce-c526fa010fd0
358145b8-ad84-4881-8dc0-8663ad6ad2ff"""
    guid_list = cor.split("\n")


    for i in guid_list:
        update_guid(i,"phase","archived")



    update_guid("4252bfba-2fda-4b7e-868c-de2cb8ed5518","phase","archived")