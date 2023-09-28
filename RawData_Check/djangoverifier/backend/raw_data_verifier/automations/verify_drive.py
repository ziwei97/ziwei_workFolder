import pandas as pd
import os
import json
import re
import csv
"""
The purpose of this file is to:
1. Extract key features pertained to the raw image data sent through the portable drive from clinical sites to SMD. 
2. Verify that the log in TransferVerification_*.xlsx mathces with the actual data
3. Extract information of the size of the file (the screenshot part in the original word doc)
"""


class VerifyDrive:

    SITE_EQ_TABLE = {}
    ACTION_ITEMS = {}

    def __init__(self, data_transfer_content, verification_file_obj):
        self.data_transfer_content = data_transfer_content
        self.verification_file_obj = verification_file_obj

    # Create a static variable that is an empty dictionary
    def printDrivePassword(path): 
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(path)

        # Convert the DataFrame to a dictionary
        dictionary = df.set_index(df.columns[0]).to_dict()[df.columns[1]]

        # Print the dictionary
        print(dictionary)

    def processDataTransferFile(self, file_path):
        """
        Verify: 
        1. the portable drive equipment ID (EQ)
        2. time range for the data transfer
        3. data transfer date
        4. patient count
        5. image collection count
        Variables are:
        f: DataTransfer.txt file
        arrive_date: the date the portable drive arrives at SMD
        """

        f = self.data_transfer_content
        # Read the DataTransfer.txt file into a pandas DataFrame
        df = pd.DataFrame([l.rstrip().split(',') for l in f.split("\n") if l != "" and not any(s in l for s in ["Size:", "New device info"])])
        # Read the first line of the file, convert it into a list where each item is seperated by the comma
        site = df.iloc[0,1].replace(' ', '').lower()        
        eq_num = self.SITE_EQ_TABLE.get(site, None)
        if eq_num:
            eq_num = int(eq_num.split('-')[1])

        # Find the portable drive equipment ID (EQ)
        serial_id = df.iloc[0,2]

        # Calculate the time range for the data transfer
        # iterate through each line, stop when the first "DirAppended" appears
        start = ""
        for line in df.iloc:
            # if anything in ACTION_ITEMS appear in line[1]
            if any(action in line[1] for action in self.ACTION_ITEMS):
                start = line[0].split(' ')[0]
                break
    
        end = df.iloc[-1,0].split(' ')[0]
        range = start + " - " + end
        name = file_path.split("/")[-2].upper()

        data_type = "DFU" if "DFU" in file_path else "Burn"
        
        # Return a dictionary containing eq, range, data_transfer_date, patient_count, and image_collection_count
        resDict = { "path": file_path, 
                    "name": name, 
                    "eq_number": eq_num, 
                    "serial_id": serial_id, 
                    "data_acquisition_time_range": range, 
                    "file_type": data_type}
        
        return resDict

    def checkTransferVerificationLog(self):
        """
        Verify that the log in TransferVerification_*.xlsx mathces with the actual data
        """
        df = pd.read_excel(self.verification_file_obj)
        images = set()
        # Find the number of image collections in the log
        # transfer_verification_log = pd.read_excel(verification_files[0], header=None)
        image_collection_count = 0
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            ln = row[0]
            if "AcquisitionData.txt" in ln and not RawDataProcessor.isFakePatient(ln): #fake patient
                image_collection_count += 1
                # ln looks like: D:\SpectralView\Diabetic_Foot_Ulcer\Patient_207-001\Right_PlantarToes_1\ImageColl_49\AcquisitionData.txt
                # I want to append Patient_207-001/Right_PlantarToes_1/ImageColl_49 to images
                newStr = ln.split("Diabetic_Foot_Ulcer\\")[1].replace("\\", "/").replace("/AcquisitionData.txt", "")
                newStr = newStr.replace("Patient_203-005", "Patient_203-003").replace("Patient_105", "Patient_205").replace("Patient_211-01", "Patient_211-001")
                images.add(newStr)
    
        return image_collection_count, images
     
    def convertSizeUnit(size):
        return str(round(size/1024**3, 2)) + " GB" if size > 1024**3 \
                else str(round(size/1024**2, 2)) + " MB" if size > 1024**2 \
                else str(round(size/1024, 2)) + " KB" if size > 1024 else str(size) + " B"           
    
    def sizeOf(self, path):
        """
        Find the size of the file in GB
        """
        # find the size of the path if path exists
        if os.path.exists(path):
            size = os.path.getsize(path)

            # return the size. if it in the biggest unit that is not zero. Rount in two decimal places.
            return self.convertSizeUnit(size)
        return None

class DFUVerifyDrive(VerifyDrive):
    ACTION_ITEMS = {'Appended'}
    SITE_EQ_TABLE = {'circleville': 'EQ-363', 'houston': 'EQ-367', 'northwell': 'EQ-368', 'eliverpool': 'EQ-399', 'hilliard': 'EQ-403', 'memphis': 'EQ-404', 'mentor': 'EQ-359', 'youngstown': 'EQ-420', 'grovecity': 'EQ-421', 'losangeles': 'EQ-427'}

    def __init__(self, data_transfer_path, verification_file):
        super().__init__(data_transfer_path, verification_file)
    
    def processDataTransferFile(self, path):
        return super().processDataTransferFile(path)
    
    def checkTransferVerificationLog(self):
        """
        Verify that the log in TransferVerification_*.xlsx mathces with the actual data
        """
        df = pd.read_excel(self.verification_file_obj)
        images = set()
        # Find the number of image collections in the log
        # transfer_verification_log = pd.read_excel(verification_files[0], header=None)
        image_collection_count = 0
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            ln = row[0]
            if "AcquisitionData.txt" in ln and not RawDataProcessor.isFakePatient(ln): #fake patient
                image_collection_count += 1
                # ln looks like: D:\SpectralView\Diabetic_Foot_Ulcer\Patient_207-001\Right_PlantarToes_1\ImageColl_49\AcquisitionData.txt
                # I want to append Patient_207-001/Right_PlantarToes_1/ImageColl_49 to images
                newStr = ln.split("Diabetic_Foot_Ulcer\\")[1].replace("\\", "/").replace("/AcquisitionData.txt", "")
                newStr = newStr.replace("Patient_203-005", "Patient_203-003").replace("Patient_105", "Patient_205").replace("Patient_211-01", "Patient_211-001")
                images.add(newStr)
    
        return image_collection_count, images
        # return super().checkTransferVerificationLog()

class BurnVerifyDrive(VerifyDrive):
    ACTION_ITEMS = {'Appended', 'Edited', 'DELETED'}
    SITE_EQ_TABLE = {'umcnola': 'EQ-311', 'chnola': 'EQ-310', 'medstar': 'EQ-309', 'mgh': 'EQ-359', 'uabed': 'EQ-360', 'uab': 'EQ-366', 'wf': 'EQ-318', 'muscmain': 'EQ-326', 'muscch': 'EQ-327', 'yale': 'EQ-336', 'phoenix': 'EQ-362', 'stonybrook': 'EQ-364', 'phillych': 'EQ-402'}
    def __init__(self, data_transfer_path, verification_file):
        super().__init__(data_transfer_path, verification_file)
    
    def processDataTransferFile(self, arrive_date):
        """
        Verify that the log in TransferVerification_*.xlsx mathces with the actual data
        """
        return super().processDataTransferFile(arrive_date)
    
    def checkTransferVerificationLog(self):
        """
        Verify that the log in TransferVerification_*.xlsx mathces with the actual data
        """
        df = pd.read_excel(self.verification_file_obj)
        images = set()
        # Find the number of image collections in the log
        # transfer_verification_log = pd.read_excel(verification_files[0], header=None)
        image_collection_count = 0
        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            ln = row[0]
            if "AcquisitionData.txt" in ln and not RawDataProcessor.isFakePatient(ln): #fake patient
                image_collection_count += 1
                # ln looks like: D:\SpectralView\Diabetic_Foot_Ulcer\Patient_207-001\Right_PlantarToes_1\ImageColl_49\AcquisitionData.txt
                # I want to append Patient_207-001/Right_PlantarToes_1/ImageColl_49 to images
                newStr = ln.split("Burn\\")[1].replace("\\", "/").replace("/AcquisitionData.txt", "")
                newStr = newStr.replace("Patient_203-005", "Patient_203-003").replace("Patient_105", "Patient_205").replace("Patient_211-01", "Patient_211-001")
                images.add(newStr)
    
        return image_collection_count, images
        # return super().checkTransferVerificationLog()



class RawDataProcessor:

    def isFakePatient(path):
        '''
        Fake patient pattern: contains 0000, 99, 98, or 97 in the path name
        '''
        # Create a regex pattern that matches the fake patient folder name
        fake_patient_pattern = re.compile(r'0000|99|98|97')

        # return true if the folder name matches the fake patient pattern
        # return false if the folder name matches the real patient pattern
        if fake_patient_pattern.search(path) is not None:
            return True
        else:
            return False

    def filterFakePatient(paths):
        return [i for i in paths if not RawDataProcessor.isFakePatient(i)]
    
    def relocateDirectory(path, new_folder_name):
        '''
        Not sure where to put this function for now. Might move it to verify_drive.py later on.
        Given the current path of the SpectralView folder, move the folder to a new parent folder called new_folder_name.
        '''
        # Find the parent directory of the "SpectralView" folder in "path"
        parent = os.path.dirname(path)
        new_path = os.path.join(parent, new_folder_name)
        if not os.path.exists(new_path):
            os.makedirs(new_path) 

        # Move the SpectralView folder and all of its contents in the new path
        new_path = os.path.join(new_path, "SpectralView")
        os.rename(path, new_path)
        return new_path

    def generateOutputCSV(path, info):
        # Write the info dictionary into a csv file. The csv file is called data_transfer_info.csv
        # The csv file is located in "path"
        with open(os.path.join(path, "data_transfer_info.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=info.keys())
            writer.writeheader()
            writer.writerow(info)

    def generateOutputJson(path, info):
        # Write the info dictionary into a json file. The json file is called data_transfer_info.json
        # The json file is located in "path"
        with open(os.path.join(path, "data_transfer_information.json"), "w") as f:
            json.dump(info, f, indent=4)


# # The main function
# if __name__ == "__main__":

#     result_path = VerifyDrive.verifyDataTransfer(DRIVE_PATH)