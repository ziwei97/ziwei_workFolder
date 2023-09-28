from django.contrib import admin
from .models import DataFileInfo
from .models import GuidList
from .models import PatientImageCount

# Register your models here.
class DataFileInfoAdmin(admin.ModelAdmin):
    list_display = ('id',
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
                  "images_in_drive_without_overlap") 
    
class GuidListAdmin(admin.ModelAdmin):
    list_display = ('collectionName', 'ImageCollFolderNames', 'ImgCollGUIDs')

class PatientImageCountAdmin(admin.ModelAdmin):
    list_display = ('dataFileInfo', 'patient_id_list', 'image_count_list')

admin.site.register(DataFileInfo, DataFileInfoAdmin)
admin.site.register(GuidList, GuidListAdmin)
admin.site.register(PatientImageCount, PatientImageCountAdmin)