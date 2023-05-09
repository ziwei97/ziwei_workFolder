import os.path
import pandas as pd

from PIL import Image

def color_convert(truth_path,new_file_path):
    OG_colorKeyGT = {'Background': [0, 0, 0],
                     'Viable': [153, 102, 51],
                     'First_Degree': [255, 174, 201],
                     'Shallow_Second_Degree': [183, 179, 0],
                     'Deep_Second_Degree': [255, 127, 39],
                     'Third_Degree': [128, 128, 128],
                     'Silvadene': [164, 149, 215],
                     'Woundbed_Epinephrine': [237, 28, 36],
                     'Woundbed_Donor_Site': [163, 73, 164],
                     'Unknown_Category': [19, 255, 0],
                     'other': [255, 255, 255]}
    og_list = [tuple(OG_colorKeyGT[i]) for i in OG_colorKeyGT]

    SageMaker_colorKeyGT = {'Background': [188, 189, 34],
                            'Viable': [148, 103, 189],
                            'First_Degree': [44, 160, 44],
                            'Shallow_Second_Degree': [31, 119, 180],
                            'Deep_Second_Degree': [255, 127, 14],
                            'Third_Degree': [214, 39, 40],
                            'Silvadene': [127, 127, 127],
                            'Woundbed_Epinephrine': [140, 86, 75],
                            'Woundbed_Donor_Site': [227, 119, 194],
                            'Unknown_Category': [19, 255, 0],
                            'other': [255, 152, 150]}

    sg_list = [tuple(SageMaker_colorKeyGT[i]) for i in SageMaker_colorKeyGT]

    img = Image.open(truth_path)
    img = img.convert("RGB")

    d = img.getdata()
    new_image = []

    for item in d:
        if item in sg_list:
            match = sg_list.index(item)
            new_image.append(tuple(og_list[match]))
        else:
            new_image.append(item)

    img.putdata(new_image)
    img.save(new_file_path)


# file=pd.read_excel('/Users/ziweishi/Desktop/phase4_guid.xlsx')








# list1 = os.listdir(folder_path)
#
# for i in list1:
#     if ".DS"  not in i:
#         path =os.path.join(folder_path,i)
#         sub = os.listdir(path)
#         for j in sub:
#             print(j)

#
# index =1
#
# for i in issue_list:
#     print(index)
#     folder_path = "/Users/ziweishi/Desktop/data_check"
#     guid_path = os.path.join(folder_path,i)
#     file_list = os.listdir(guid_path)
#     truth_path = [os.path.join(guid_path, f) for f in file_list if 'Truth' in f][0]
#     new_file_name = "Converted_Final_"+i+".png"
#     new_truth_path = os.path.join(guid_path,new_file_name)
#     color_convert(truth_path,truth_path)
#     index+=1
