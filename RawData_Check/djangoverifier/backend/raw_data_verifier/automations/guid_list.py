import mysql.connector
import glob
import pandas as pd
import os
import openpyxl
from decouple import config


class GUIDListGenerator:
    def __init__(self, sql_file_obj, verification_file_obj, name):
        sql_file_obj.seek(0)  # Reset the file pointer to the beginning
        self.sql_content = sql_file_obj.read().decode('utf-8') # Read the content of the file as a string
                
        self.xlsx = verification_file_obj
        self.siteName = name.split("_")[0].lower()
        # self.connection = mysql.connector.connect(user='root', password='spectralmay2306!', host='localhost')
        self.user = config('MYSQL_USER')
        self.password = config('MYSQL_PASSWORD')
        self.host = config('MYSQL_HOST')

        self.connection = mysql.connector.connect(user=self.user, password=self.password, host=self.host)

        self.cursor = self.connection.cursor()

        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS DFU_{self.siteName}")
        self.cursor.execute(f"USE DFU_{self.siteName}")
        for query in self.sql_content.split(";"):
            if query.strip():
                self.cursor.execute(query)

        # for statement in self.sql_content.split(";"):
        #     if statement.strip():
        #         self.cursor.execute(statement)

        self.connection.commit()

        query = f"SELECT ic.ImageCollFolderName, ic.ImgCollGUID, i.ImageFileName, i.ImageType \
        FROM DFU_{self.siteName}.imagescollection as ic \
            INNER JOIN DFU_{self.siteName}.images as i \
                ON ic.IMCOLLID = i.IMCOLLID;"

        # query = "select * from imagescollection left join injury on imagescollection.INJURYID = injury.INJURYID left join patient on injury.PID = patient.PID"

        self.cursor.execute(query)

        # Fetch all the corresponding values
        self.all_imgs_info = self.cursor.fetchall()


    def get_list_collections(self):
        '''Get a list of img collections from verification file and store in a set
        '''

        verification_file_obj = self.xlsx
        image_collection_set = set()

        # Create dataframe for the sheet seperated by each row in the sheet
        transfer_verification_log = pd.read_excel(verification_file_obj)
        for _, row in transfer_verification_log.iterrows():
            # Print the contents of each row
            ln = row[0]
            if "ImageColl_" in ln:
                image_collection_set.add(ln.rsplit("\\", maxsplit=1)[0])
        
        return image_collection_set


    def filter_most_recent(self):
        '''the sql file contains both old and new data.
        Filter out the old data and only keep the ones that are in the current data transfer
        '''
        excel_content = self.get_list_collections() # set of image collection names from excel file

        results = self.all_imgs_info
        guid_lst = set()
        types = {}
        patient_group = {}

        for row in results:
            shortened = row[0]
            if shortened in excel_content:
                shortened = shortened.replace("Patient_203-005", "Patient_203-003").replace("Patient_105", "Patient_205").replace("Patient_211-01", "Patient_211-001")
                patient_id = shortened.split("\\")[3]
                if patient_id not in patient_group:
                    patient_group[patient_id] = {}
                content = (shortened, row[1])
                if content not in guid_lst:
                    guid_lst.add(content)
                img_type = row[3].replace(" ", "_")
                types[img_type] = types.get(row[3].replace(" ", "_"), 0) + 1
                patient_group[patient_id][img_type] = patient_group[patient_id].get(img_type, 0) + 1
        return guid_lst, types, patient_group

    
    def generate_img_collections_details(self):
        '''generate GUID List and Image Type Stats'''
        guid_lst, type_counts, patient_group = self.filter_most_recent()
        # print("guid_lst: ", guid_lst)

        # print the results in an excel file of two colums, where the first column is ImageCollFolderName and the second column is ImgCollGUID
        df = pd.DataFrame(guid_lst, columns=["ImageCollFolderName", "ImgCollGUID"])      

        return df, type_counts, patient_group

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
    
# main
if __name__ == "__main__":
    files_dict = {"/Volumes/dfu/DataTransfers/mentoh/DFU_SS/MENTOH_DFU_SMD2225-017_09_08_23/SpectralView/dvsspdata.sql": "mentoh"}
    file_ver = "/Volumes/dfu/DataTransfers/mentoh/DFU_SS/MENTOH_DFU_SMD2225-017_09_08_23/SpectralView/TransferVerification_2023-08-30_13_59.xlsx"
    for path, siteName in files_dict.items():
        print(path)
        print(siteName)
        a = GUIDListGenerator(path,file_ver,siteName)
        list = a.get_list_collections()
        print(list[0])
