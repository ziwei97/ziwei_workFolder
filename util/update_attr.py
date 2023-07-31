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

    update_guid("4252bfba-2fda-4b7e-868c-de2cb8ed5518","phase","archived")