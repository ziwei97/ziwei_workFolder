import boto3
import pickle
import pathlib
import pandas as pd
import os
import numpy as np

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

path = "../Documents/Database/"

def load_db(file_path: str) -> list:
    '''Loads the give json file with the data'''
    # Validate file existence
    if not os.path.exists(file_path):
        print(f'[ERROR] File path {file_path} does not exist')
        return None
    with open(file_path, 'rb') as file:
        _object = pickle.load(file)
        file.close()
    return _object

def get_table(table_name, refresh=False):

    file_path = os.path.join(path,f'{table_name}.pickle')

    # if not pathlib.Path(file_path).exists() or refresh:
    #     # print(f'No database file for {table_name} found. Downloading file:')
    update_db_file(table_name)

    return load_db(file_path)



def update_db_file(table_name: str, debug: bool = True) -> list:
    '''Updates a file with the most current data from the DBs'''
    # User confirmation
    temp = input(f'Press "enter" to continue querying "{table_name}"')
    print("Starting...")

    # pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    path_load = os.path.join(path,f'{table_name}.pickle')

    try:
        dynamo_table = dynamodb.Table(table_name)
    except Exception as e:
        print(f'There was an issue loading the table: {table_name}.\n{e}')
        return []

    # begin query
    raw_response = dynamo_table.scan()
    data = raw_response['Items']

    # for large queries
    while 'LastEvaluatedKey' in raw_response:
        if debug:
            if "LastEvaluatedKey" in raw_response:
                print(f'Making a new request starting at {raw_response["LastEvaluatedKey"]}')
        raw_response = dynamo_table.scan(ExclusiveStartKey=raw_response['LastEvaluatedKey'])
        data.extend(raw_response['Items'])

    # output query
    if debug:
        print(f'Total retrieved entries: {len(data)}')

    try:
        with open(path_load, 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            file.close()
    except Exception as e:
        print(data)
        print(f'There was an issue writing data to {path_load}.\n{e}')



def download_table(table_name):
    a = input("Refresh database yes or no: ")
    excel_path = os.path.join(path,table_name+".xlsx")
    pickle_path = excel_path.replace(".xlsx",".pickle")
    if a =="yes":
        if os.path.isdir(excel_path) ==True:
            os.remove(excel_path)
        if os.path.isdir(pickle_path) ==True:
            os.remove(pickle_path)
        df1 = get_table(table_name)
        df = pd.DataFrame(df1)
        df.to_excel(excel_path)
        df = pd.read_excel(excel_path)
    else:
        df = pd.read_excel(excel_path)
    return df

if __name__ == "__main__":
    # burn= download_table("DFU_Master_ImageCollections")
    # final1 = burn[burn["StudyName"]=="BURN_BTS"]
    # final = final1[["ImgCollGUID","Bucket","Status","SubjectID","PseudoColor","Assessing","Raw","Mask","Tags"]]
    # final.to_excel("/Users/ziweishi/Desktop/BURN.xlsx")

    a = download_table("DFU_Master_ImageCollections")

    a = a[["ImgCollGUID","phase","StudyType","Bucket","Status","SubjectID","PseudoColor","Assessing","Raw","Mask","Tags"]]

    # a.to_excel("/Users/ziweishi/Desktop/dfuu.xlsx")





















