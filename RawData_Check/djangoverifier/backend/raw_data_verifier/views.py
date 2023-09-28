from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DataFileInfoSerializer, GuidListSerializer, PatientImageCountSerializer
from .models import DataFileInfo, GuidList
from .automations.verify_drive import DFUVerifyDrive, BurnVerifyDrive
from .automations.guid_list import GUIDListGenerator
import pandas as pd
from io import BytesIO
from .models import GuidList, DataFileInfo, PatientImageCount
from smb.SMBConnection import SMBConnection
from decouple import config
import socket
import datetime
import tempfile
from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache 


# Create your views here.
class DataFileInfoView(viewsets.ModelViewSet):
    serializer_class = DataFileInfoSerializer
    queryset = DataFileInfo.objects.all()
    
    def getImgCollStats(sql, xlsx, data_transfer_info):
        '''Given the verification xlsx file and the data_transfer_info dictionary of the data transfer info,
        generate GuidList model and populate the guidListID and images_count of data_transfer_info
        finally, return a dictionary with key being the patient_id and value being the image collection count for each type of image'''
        verifier = GUIDListGenerator(sql, xlsx, data_transfer_info["name"])

        df, type_counts, patient_categories = verifier.generate_img_collections_details()
        # Retrieve or create the associated Detail object
        guids = GuidList.objects.create()
        guids.collectionName = data_transfer_info["name"].split("_")[0].lower()
        guids.ImageCollFolderNames = ",".join(df["ImageCollFolderName"].tolist())
        guids.ImgCollGUIDs = ",".join(df["ImgCollGUID"].tolist())
        guids.save()

        data_transfer_info["guidListID"] = guids.id
        data_transfer_info["images_count"] = sum(type_counts.values())
        # add content of type_counts to data_transfer_info
        data_transfer_info.update(type_counts)
        return patient_categories

def hello(request):
    data = {
        'message': 'Hello, World!'
    }
    return JsonResponse(data)


def homePage(request):
    return render(request,"homePage.html")




@never_cache
def delete_data_file_info(request, file_path):
    # Delete the file from the database
    try:
        item = DataFileInfo.objects.get(path=file_path + "/SpectralView")
        if item:
            guidListID = item.guidListID
            if guidListID:
                guidList = GuidList.objects.get(id=guidListID)
                guidList.delete()
            item.delete()
    except DataFileInfo.DoesNotExist:
        pass
    return HttpResponse(status=200)

    
class GuidListView(viewsets.ModelViewSet):
    serializer_class = GuidListSerializer
    queryset = GuidList.objects.all()

class PatientImageCountView(viewsets.ModelViewSet):
    serializer_class = PatientImageCountSerializer
    queryset = PatientImageCount.objects.all()


class ServerConnectionsView(viewsets.ModelViewSet):

    def perform_smb_info_query(item_path):
        '''
        Given an item_path of a data collection in the local server, return all the data info
        Return the info data, as well as the data for populating PatientImageCount
        We also return the patient_groups, which is a dictionary of patient_id and image collection count for each type of image
        '''
        shared_folder_name = item_path.split("/")[0]
        item_path += "/SpectralView"
        item_sub_path = item_path.replace(shared_folder_name + "/", "")
        # item_path = 'DFU/DataTransfers/memdfu/DFU_SS/MEMDFU_DFU_SMD2051-008_06_26_23/SpectralView'
        smb_connection = ServerConnectionsView.establish_smb_connection() # Maybe save this in a cach or something

        file_list = smb_connection.listPath(shared_folder_name, item_sub_path)
        
        verification_file_obj, sql_file_obj = tempfile.NamedTemporaryFile(), tempfile.NamedTemporaryFile()
        data_transfer_content, data_transfer_path, verification_path = "", "", ""
        
        for file in file_list:
            if file.filename.startswith("TransferVerification") and "Biopsy" not in file.filename:
                # Go into this xlsx file, and print each line
                verification_path = f"{item_sub_path}/{file.filename}"
                smb_connection.retrieveFile(shared_folder_name, verification_path, verification_file_obj)
            elif file.filename == "DataTransfer.txt":
                data_transfer_path = f"{item_sub_path}/{file.filename}"
                with open('local_file.txt', 'wb') as local_file:
                    smb_connection.retrieveFile(shared_folder_name, data_transfer_path, local_file)
                with open('local_file.txt', 'r') as local_file:
                    data_transfer_content = local_file.read()
            elif ".sql" in file.filename:
                sql_path = f"{item_sub_path}/{file.filename}"
                smb_connection.retrieveFile(shared_folder_name, sql_path, sql_file_obj)
        
        if "DFU" in item_path:
            verifier = DFUVerifyDrive(data_transfer_content, verification_file_obj)
        elif "EPOC" in item_path:
            verifier = BurnVerifyDrive(data_transfer_content, verification_file_obj)
        info = verifier.processDataTransferFile(item_path)
        patient_groups = DataFileInfoView.getImgCollStats(sql_file_obj, verification_file_obj, info)
         # TODO: return actual list in verifier.checkTransferVerificationLog() 
        info["image_coll_count_in_verification_excel"], images_in_excel = verifier.checkTransferVerificationLog() 

        spectral_view_path = "/" + item_sub_path 
        # TODO: return actual list in ServerConnectionsView.get_server_file_info(smb_connection, shared_folder_name, spectral_view_path)
        spectral_view_size_on_drive, Pictures_size_on_drive, patient_count, image_coll_count_in_drive, images_on_drive = ServerConnectionsView.get_server_file_info(smb_connection, shared_folder_name, spectral_view_path)
        info["spectral_view_size_on_drive"] = spectral_view_size_on_drive
        info["Pictures_size_on_drive"] = Pictures_size_on_drive
        info["patient_count"] = patient_count
        info["image_coll_count_in_drive"] = image_coll_count_in_drive
        
        print("in excel: ")
        print(images_in_excel)
        print("in drive: ")
        print(images_on_drive)
        
        # given two sets, find the non-overlapping elements in each set
        intersection = images_in_excel.intersection(images_on_drive)
        images_in_excel_without_overlap = images_in_excel.difference(intersection)
        images_on_drive_without_overlap = images_on_drive.difference(intersection)

        diff_log = {}
        diff_log["images_in_excel_without_overlap"] = images_in_excel_without_overlap
        diff_log["images_on_drive_without_overlap"] = images_on_drive_without_overlap

        
        return info, patient_groups, diff_log
    
    def get_server_file_info(smb_connection, shared_folder_name, spectral_view_path):
        total_size = 0
        file_list = smb_connection.listPath(shared_folder_name, spectral_view_path)
        for file_entry in file_list:
            file_name = file_entry.filename
            if file_name not in ['.', '..']:
                if not file_entry.isDirectory:
                    total_size += file_entry.file_size
        if shared_folder_name == "DFU":
            sub_path = spectral_view_path + "/Diabetic_Foot_Ulcer"
        elif shared_folder_name == "EPOC":
            sub_path = spectral_view_path + "/Burn"
        dfu_size, patient_count, image_coll_count_in_drive, images = ServerConnectionsView.get_server_file_info_helper(smb_connection, shared_folder_name, sub_path)
        return DFUVerifyDrive.convertSizeUnit(total_size + dfu_size), DFUVerifyDrive.convertSizeUnit(dfu_size), patient_count, image_coll_count_in_drive, images
                    
    def get_server_file_info_helper(smb_connection, shared_folder_name, sub_path):
        
        total_size, patien_count, imgColl_count = 0, 0, 0
        images = set()

        # Get a list of files and subdirectories within the folder
        file_list = smb_connection.listPath(shared_folder_name, sub_path)
        for file_entry in file_list:
            file_name = file_entry.filename

            # Exclude the current and parent directory entries
            if file_name not in ['.', '..']:
                file_path = f"{sub_path}/{file_name}"

                # Check if the entry is a file or subdirectory
                if file_entry.isDirectory:
                    # Recursively get the size of the subdirectory
                    if "Patient" in file_name and not any(x in file_name for x in ["0000", "99", "98", "97"]):
                        patien_count += 1
                    if "ImageColl_" in file_name and not any(x in file_path for x in ["0000", "99", "98", "97"]):
                        imgColl_count += 1
                        if "DFU" in file_path:
                            # str: /DataTransfers/grovoh/DFU_SS/GROVOH_DFU_SMD2225-013_07_11_23/SpectralView/Diabetic_Foot_Ulcer/Patient_208-014/Right_Plantar_1/ImageColl_6
                            # want: Patient_208-014/Right_Plantar_1/ImageColl_6
                            newStr = "/".join(file_path.split("/")[7:10])
                        elif "BURN" in file_path:
                            # str: /DataTransfers/chphil/CHPHIL_BURN_SMD2138-016_03_13_23/SpectralView/Burn/Patient_111004/Injury_1/Ant.R.L.Trunk/Inferior/ImageColl_2
                            # want: Patient_111004/Injury_1/Ant.R.L.Trunk/Inferior/ImageColl_2
                            newStr = "/".join(file_path.split("/")[6:11])
                        newStr = newStr.replace("Patient_203-005", "Patient_203-003").replace("Patient_105", "Patient_205").replace("Patient_211-01", "Patient_211-001")
                        images.add(newStr)
                    subdirectory_size, sub_patient_size, sub_imgColl_size, sub_images = ServerConnectionsView.get_server_file_info_helper(smb_connection, shared_folder_name, file_path)
                    total_size += subdirectory_size
                    patien_count += sub_patient_size
                    imgColl_count += sub_imgColl_size
                    images.update(sub_images)
                else:
                    # Add the size of the file to the total
                    total_size += file_entry.file_size
        
        return total_size, patien_count, imgColl_count, images

    def establish_smb_connection(self):
        # Server connection details. Information is encrypted. 
        server_ip = config('REMOTE_SERVER_IP')
        server_username = config('REMOTE_SERVER_USERNAME')
        server_password = config('REMOTE_SERVER_PASSWORD')
        my_name = socket.gethostname()
        remote_name = config('REMOTE_NAME')

        # Create an SMB connection object
        smb_connection = SMBConnection(server_username, server_password, my_name, remote_name, domain="spectralmd.com", use_ntlm_v2=True, is_direct_tcp=True)
        # Connect to the remote server
        connected = smb_connection.connect(server_ip, port=445)        
        # Return the SMB connection object
        return smb_connection

    @never_cache
    def get_remote_files(request, data_type): 
        '''Get all the remote files. If data_type is DFU, get all the DFU files,
        likewise if data_type is Burn, get all the EPOC files'''

        print("The Start of get_remote_files function")
        # cache_key = "file_list"
        shared_folder_name = data_type

        # Attempt to get the data from the cache
        subfolders = None
        if subfolders is None:
            print("subfolders is not cached previously")
            # Establish the SMB connection
            smb_connection = ServerConnectionsView.establish_smb_connection()

            # List files in the shared folder
            data_transfers_folder = '/DataTransfers'

            # Get the list of files in the DataTransfers directory
            file_list = smb_connection.listPath(shared_folder_name, data_transfers_folder)
        
            subfolders = []
            site_stats = {}
            for file in file_list:
                # Check if it's a directory (ignoring . and ..)
                if file.isDirectory and file.filename not in ['.', '..']:
                    # Get the list of files in the subfolder
                    subfolder_path = data_transfers_folder + '/' + file.filename # e.g. /DataTransfers/awcm
                    subfolder_files = smb_connection.listPath(shared_folder_name, subfolder_path)
                    
                    for subfile in subfolder_files:
                        # Check if it's a second-level subdirectory (ignoring . and ..)
                        if subfile.isDirectory and subfile.filename not in ['.', '..', 'DFU_SSP', 'BURN_BTS']:
                            # Get the list of files in the second-level subfolder
                            subfolder_path = data_transfers_folder + '/' + file.filename + '/' + subfile.filename # e.g. /DataTransfers/awcm/DFU_SS
                            next_level_files = smb_connection.listPath(shared_folder_name, subfolder_path)
                            if shared_folder_name == "EPOC" and '(' not in subfolder_path and ')' not in subfolder_path:
                                creation_time = datetime.datetime.fromtimestamp(subfile.create_time).strftime('%Y-%m-%d %H:%M:%S')
                                subfolders.append((shared_folder_name + subfolder_path, creation_time))
                                site_name = (shared_folder_name + subfolder_path).split("/")[2]
                                site_stats[site_name] = site_stats.get(site_name, 0) + 1
                            elif shared_folder_name == "DFU":
                                # Print out the files in the second-level subfolder
                                for next_file in next_level_files:
                                    if next_file.filename not in ['.', '..', '.DS_Store'] and ')' not in next_file.filename and '(' not in next_file.filename:
                                        sub_subfolder_path = shared_folder_name + data_transfers_folder + '/' + file.filename + '/' + subfile.filename + '/' + next_file.filename # e.g. /DataTransfers/awcm/DFU_SS/AWCM_DFU_SMD2037-004_03_25_2021
                                        # I want to print out every nested files residing within sub_subfolder_path                                        
                                        creation_time = datetime.datetime.fromtimestamp(next_file.create_time).strftime('%Y-%m-%d %H:%M:%S')
                                        subfolders.append((sub_subfolder_path, creation_time))
                                        site_name = sub_subfolder_path.split("/")[2]
                                        site_stats[site_name] = site_stats.get(site_name, 0) + 1
            # Close the SMB connection
            smb_connection.close()
            subfolders.sort(key=lambda x: x[1], reverse=True)
        # Return the subfolder list as a JSON response
        return JsonResponse({'subfolders': subfolders, 'site_stats': site_stats})
    
    @never_cache
    def get_cached_items(request, data_type):
        return ServerConnectionsView.get_remote_files(request, data_type)
    
@never_cache
def handle_info_click(request, itemPath, arrival_date_time):
    '''Handle the click on the info button. Given the itemPath and arrival_date_time,
    locate the file in local server, and do all the analysis,
    create the DataFileInfo object that contains all the analysis info,
    create the GuidList and PatientImageCount objects associated with the DataFileInfo object,
    and return the id of the DataFileInfo object in the response
    '''
    # The path: DFU/DataTransfers/memdfu/DFU_SS/MEMDFU_DFU_SMD2051-008_06_26_23 
    # shared_folder_name = 'DFU'
    # sub folders = 'DataTransfers/memdfu/DFU_SS/MEMDFU_DFU_SMD2051-008_06_26_23/SpectralView'
    # File we are looking for in there: Verification.xlsx and DataTransfer.txt
    item = None
    try:
        # Check if the item exists in the database
        item = DataFileInfo.objects.get(path=itemPath + "/SpectralView")
        print("Item exists in the database")
        
    except DataFileInfo.DoesNotExist:
        print("Item does not exist in the database")
        # Item does not exist in the database, retrieve it from the SMB query
        smb_item, patient_group, diff_log = ServerConnectionsView.perform_smb_info_query(itemPath)  # Replace with your SMB query logic
        smb_item["data_transfer_date"] = arrival_date_time
        smb_item['is_match'] = smb_item['image_coll_count_in_drive'] == smb_item['image_coll_count_in_verification_excel']
        
        # convert diff_log["images_in_excel_without_overlap"] to string
        smb_item['images_in_excel_without_overlap'] = ",".join(diff_log["images_in_excel_without_overlap"])
        smb_item['images_in_drive_without_overlap'] = ",".join(diff_log["images_on_drive_without_overlap"])

        # Create a new Item using all the fields of smb_item
        item = DataFileInfo.objects.create(**smb_item)
        
        new_patient_id_list, new_image_count_list = create_PatientImageCount_fields(patient_group)
        patientImageCount = PatientImageCount.objects.create(dataFileInfo=item, patient_id_list=new_patient_id_list, image_count_list=new_image_count_list)
        patientImageCount.save()

        item.PatientImageCountID = patientImageCount.id
        item.save()

    # Return the item data in the response
    return JsonResponse({'id': item.id})


def create_PatientImageCount_fields(patient_group):
    '''
    patient_group is a dictionary with key being the patient_id and value being the image collection count for each type of image associated with that patient
    turn that data into valid fields for PatientImageCount model
    Which is a string of patient_id_list and image_count_list, joined by ";"
    '''
    patient_id_list, image_count_list = [], []
    for k, v in patient_group.items():
        patient_id_list.append(k)
        image_count_list_per_patient = []
        for img_type, count in v.items():
            image_count_list_per_patient.append(img_type + ":" + str(count))
        img_count_str = ",".join(image_count_list_per_patient)
        image_count_list.append(img_count_str)
    return ";".join(patient_id_list), ";".join(image_count_list)
