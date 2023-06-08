import os.path
import pymysql
import pandas as pd
import numpy as np
import download_whole_dynamodb_table



def server_table_output(sql_path):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='szw970727',
        database='algorithm',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    path =sql_path
    with open(path, 'r') as file:
        query = file.read()

    statements = query.split(';')
    # Execute each statement
    for statement in statements:
        cursor.execute(statement)

    query1 = "select * from imagescollection left join injury on imagescollection.INJURYID=injury.INJURYID join patient on injury.PID = patient.PID"
    cursor.execute(query1)
    collection_result = cursor.fetchall()
    df = pd.DataFrame(collection_result)


    cursor.close()
    connection.close()
    return df


def substract(sql_path1,sql_path2):
    df1 = server_table_output(sql_path1)
    df2 = server_table_output(sql_path2)

    list1 = df1["ImgCollGUID"].to_list()
    list2 = df2["ImgCollGUID"].to_list()

    new=[]
    for i in list2:
        if i not in list1:
            new.append(i)

    df = df2[df2["ImgCollGUID"].isin(new)]

    site = (sql_path1.split("/"))[-5]
    site_path = '/Users/ziweishi/Documents/compare_check/' + site +"/"
    if os.path.isdir(site_path) == False:
        os.mkdir(site_path)
    file_path = site_path + site+"_new.xlsx"
    df.to_excel(file_path)
    print("done")

    return df


if __name__ =="__main__":
    hilloh = {
        "sql_path1": "/Volumes/dfu/DataTransfers/hilloh/DFU_SS/HILLOH_DFU_SMD2225-011_04_25_23/SpectralView/dvsspdata.sql",
        "sql_path2":"/Volumes/dfu/DataTransfers/hilloh/DFU_SS/HILLOH_DFU_SMD2225-011_06_01_23/SpectralView/dvsspdata.sql"
    }

    mentoh = {
        "sql_path1": "/Volumes/dfu/DataTransfers/mentoh/DFU_SS/MENTOH_DFU_SMD2223-007_03_20_23/SpectralView/dvsspdata.sql",
        "sql_path2": "/Volumes/dfu/DataTransfers/mentoh/DFU_SS/MENTOH_DFU_SMD2223-007_06_01_23/SpectralView/dvsspdata.sql"
    }

    grovoh = {
        "sql_path1":"/Volumes/dfu/DataTransfers/grovoh/DFU_SS/GROVOH_DFU_SMD2225-013_04_25_23/SpectralView/dvsspdata.sql",
        "sql_path2":"/Volumes/dfu/DataTransfers/grovoh/DFU_SS/GROVOH_DFU_SMD2225-013_06_01_23/SpectralView/dvsspdata.sql"
    }

    list = hilloh,mentoh,grovoh
    df_list = []

    df1 = server_table_output("/Volumes/dfu/DataTransfers/lahdfu/DFU_SS/LASITE_DFU_SMD2225-019_06_01_23/SpectralView/dvsspdata.sql")
    df_list.append(df1)

    for i in list:
        df = substract(i["sql_path1"],i["sql_path2"])
        df_list.append(df)

    union_df = pd.concat(df_list)
    union_df.to_excel("/Users/ziweishi/Desktop/new_dfu_check.xlsx")








