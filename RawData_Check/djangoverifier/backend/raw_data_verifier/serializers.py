from rest_framework import serializers
from .models import DataFileInfo
from .models import GuidList
from .models import PatientImageCount

class DataFileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFileInfo
        fields = ('id',
                  'path', 
                  'file_type',
                  'name',
                  'eq_number', 
                  "serial_id",
                  "data_acquisition_time_range",
                  "data_transfer_date",
                  "patient_count",
                  "images_count",
                  "image_coll_count_in_drive",
                  "image_coll_count_in_verification_excel",
                  "is_match",
                  "spectral_view_size_on_drive",
                  "Pictures_size_on_drive",
                  "Raw_MSI",
                  "Pseudocolor_generation_intermediate_output",
                  "Pseudocolor",
                  "Reference",
                  "CJA",
                  "guidListID",
                  "PatientImageCountID",
                  "images_in_excel_without_overlap",
                  "images_in_drive_without_overlap"
                  )

# Create a serializer for the GUID list as well
class GuidListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidList
        fields = ('id',
                  'collectionName',
                  'ImageCollFolderNames',
                  'ImgCollGUIDs')

class PatientImageCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientImageCount
        fields = ('id',
                  'dataFileInfo',
                  'patient_id_list',
                  'image_count_list')
        
        
