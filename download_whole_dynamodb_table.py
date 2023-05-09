import boto3
import pickle
import pathlib
import pandas as pd
import os

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

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

    file_path = os.path.join('/Users/ziweishi/Documents/database',f'{table_name}.pickle')

    if not pathlib.Path(file_path).exists() or refresh:
        # print(f'No database file for {table_name} found. Downloading file:')
        update_db_file(table_name)

    return load_db(file_path)



def update_db_file(table_name: str, debug: bool = True) -> list:
    '''Updates a file with the most current data from the DBs'''

    # User confirmation
    temp = input(f'Press "enter" to continue querying "{table_name}"')
    print("Starting...")

    # pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    path_load = os.path.join('/Users/ziweishi/Documents/database',f'{table_name}.pickle')

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


df = get_table('BURN_Master_ImageCollections')
df_final = pd.DataFrame(df)
df_final.to_excel('/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.xlsx')