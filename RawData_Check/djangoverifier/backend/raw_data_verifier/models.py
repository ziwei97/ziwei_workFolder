from django.db import models
import json

# Create your models here.
class DataFileInfo(models.Model):
    """Create a model for drive data info. The model contains the following info:
    1. path: charfield
    2. EQ number: integer
    3. serial id: charfield
    4. data transfer time range: charfield
    5. data transfer date: charfield
    6. patient count: integer
    7. image_coll_count_in_drive: integer
    8. image_coll_count_in_verification_excel: integer
    9. is_match: boolean
    10. spectral_view_size_on_drive: charfield for now. Might change to floatfield later on if decide to have one single unit.
    11. Pictures_size_on_drive: charfield for now. Might change to floatfield later on if decide to have one single unit.
    """
    path = models.CharField(max_length=255, null=True)
    # file_hash = models.CharField(max_length=255, null=True)
    file_type = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    eq_number = models.IntegerField(null=True)
    serial_id = models.CharField(max_length=255, null=True)
    data_acquisition_time_range = models.CharField(max_length=255, null=True)
    data_transfer_date = models.CharField(max_length=255, null=True)
    patient_count = models.IntegerField(null=True)
    image_coll_count_in_drive = models.IntegerField(null=True)
    image_coll_count_in_verification_excel = models.IntegerField(null=True)
    is_match = models.BooleanField(null=True)
    spectral_view_size_on_drive = models.CharField(max_length=255, null=True)
    Pictures_size_on_drive = models.CharField(max_length=255, null=True)
    guidListID = models.IntegerField(null=True)
    images_count = models.IntegerField(null=True)
    Raw_MSI = models.IntegerField(null=True, default=0)
    Pseudocolor_generation_intermediate_output = models.IntegerField(null=True, default=0)
    Pseudocolor = models.IntegerField(null=True, default=0)
    Reference = models.IntegerField(null=True, default=0)
    CJA = models.IntegerField(null=True, default=0)
    PatientImageCountID = models.IntegerField(null=True)
    # For detailed diff info
    images_in_excel_without_overlap = models.TextField(null=True)
    images_in_drive_without_overlap = models.TextField(null=True)




    def __str__(self):
        # create a string from the path
        return "Object ID: " + str(self.id) + "\n"
    
class GuidList(models.Model):
    """Create a model for GUID list. The model contains the following info:
    1. collectionName: a string
    2. ImageCollFolderNames: a list of image collection directories
    3. ImgCollGUIDs: a list of strings, each of which is a GUID
    """
    # dataFileInfo = models.ForeignKey(DataFileInfo, on_delete=models.CASCADE, null=True)
    collectionName = models.CharField(max_length=255, null=True)
    ImageCollFolderNames = models.TextField(null=True)
    ImgCollGUIDs = models.TextField(null=True)

    # def get_ImageCollFolderNames(self):
    #     return self.ImageCollFolderNames.split(",")
    
    # def getImgCollGUIDs(self):
    #     return self.ImgCollGUIDs.split(",")
    
    # def __str__(self):
    #     return self.collectionName + "\n"

class PatientImageCount(models.Model):
    """Create a model that has three fields
    1. Foreidn key associated with DataFileInfo model
    2. list of patient id
    3. list of image count, where count[i] is the # of images collected for patient[i] in DataFileInfo
    """
    dataFileInfo = models.ForeignKey(DataFileInfo, on_delete=models.CASCADE, null=True)
    patient_id_list = models.TextField(null=True)
    image_count_list = models.TextField(null=True)

    # def get_patient_id_list(self):
    #     return self.patient_id_list.split(",")
    
    # def get_image_count_list(self):
    #     return self.image_count_list.split(",")

    # def __str__(self):
    #     return "Object ID: " + str(self.id) + "\n"



        
