import boto3
import pandas as pd

dynamodb = boto3.resource('dynamodb')
table_name = 'DFU_Master_ImageCollections'  # 替换为你的 DynamoDB 表名
table = dynamodb.Table(table_name)


def update_guid(table,guid,attr,value):
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


def add_phase(df):

    guid = df["ImgCollGUID"].to_list()
    status = df["Status"].to_list()

    index=0

    for i in guid:
        sta =status[index]

        if sta =="acquired":
            update_guid(table, i, "phase", 1)
        if sta =="archived":
            update_guid(table,i,"phase","archived")

        index+=1









if __name__ == "__main__":
    # update_guid(table,"cc6b7a51-e271-4725-a920-e925bb0aa347","StudyType","validation")

    path = "/Users/ziweishi/Documents/DFU_regular_update/20230807val/20230807val_Guid_list.xlsx"
    df = pd.read_excel(path)
    add_phase(df)


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



