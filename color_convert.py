import os

import pandas as pd
import numpy as np
from PIL import Image
import boto3
from download_request import download_raw,get_attribute


s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')


def OverlayMask(path):
    img = Image.open(path)
    Mask = np.array(img)

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

    SageMaker_colorKeyGT = {'Background': [188, 189, 34],
                            'Viable': [140, 105, 67],
                            'First_Degree': [233, 181, 199],
                            'Shallow_Second_Degree': [182, 178, 79],
                            'Deep_Second_Degree': [225, 138, 79],
                            'Third_Degree': [214, 39, 40],
                            'Silvadene': [127, 127, 127],
                            'Woundbed_Epinephrine': [140, 86, 75],
                            'Woundbed_Donor_Site': [227, 119, 194],
                            'Unknown_Category': [154, 247, 104],
                            'other': [255, 152, 150]}

    r = Mask[:, :, 0]
    g = Mask[:, :, 1]
    b = Mask[:, :, 2]

    for key in SageMaker_colorKeyGT.keys():
        # find index1 & index2 & index3 overlay part
        index1 = (r == SageMaker_colorKeyGT[key][0]) * 1
        index2 = (g == SageMaker_colorKeyGT[key][1]) * 1
        index3 = (b == SageMaker_colorKeyGT[key][2]) * 1
        index = index1 + index2 + index3
        final_index = index == 3
        Mask[final_index, 0] = OG_colorKeyGT[key][0]
        Mask[final_index, 1] = OG_colorKeyGT[key][1]
        Mask[final_index, 2] = OG_colorKeyGT[key][2]

    new_image = Image.fromarray(Mask)
    new_image.save(path)

def return_pixel_type(path):
    img = Image.open(path)
    image_array = np.array(img)
    # 获取图像的形状（高度、宽度、通道数）
    height, width, channels = image_array.shape
    # 创建一个空数组来存储RGB颜色
    int_array = image_array.astype(int)
    list = []
    tuple_list = []
    # 遍历图像的每个像素
    for i in range(height):
        for j in range(width):
            # 获取像素的RGB值
            rgb = int_array[i, j]
            a = str(rgb[0]) + "," + str(rgb[1]) + "," + str(rgb[2])
            if a not in list:
                s = a.split(",")
                sub_list = []
                for c in s:
                    sub_list.append(int(c))
                    sub_list1 = tuple(sub_list)
                list.append(a)
                tuple_list.append(sub_list1)
    return tuple_list

if __name__ == "__main__":
    # table_name = 'BURN_Master_ImageCollections'
    # table = dynamodb.Table(table_name)
    #
    # df_guid = pd.read_excel("/Users/ziweishi/Desktop/phase5.xlsx")
    # guid_list =df_guid["ImgCollGUID"].to_list()
    # attrs=["Mask"]
    # download_raw(table,guid_list,attrs,"/Users/ziweishi/Desktop/Burn_Mask")
    #
    # index=0
    # for i in guid_list:
    #     print(index)
    #     fold = "/Users/ziweishi/Documents/MASK_convert/"
    #     path = fold+i+"/Mask_"+i+".png"
    #     OverlayMask(path)
    #     bucket =get_attribute(table,i,"Bucket")
    #     s3_path = "Mask/Mask_"+i+".png"
    #     # print(s3_path)
    #     # s3.Bucket(bucket).upload_file(path, s3_path)
    #     index+=1


    # Create a uint8 array
    # uint8_array = np.array([10, 20, 30], dtype=np.uint8)
    #
    # # Convert uint8 array to int
    # int_array = uint8_array.astype(int)
    #
    # # Print the int array
    # print(int_array)
    pixel_file = {}
    path = "/Users/ziweishi/Desktop/WASP_Mask/"
    list = os.listdir(path)
    index=0
    for i in list:
        if i[0] != ".":
            img_path = path+i+"/Mask_"+i+".png"
            tuple_list = return_pixel_type(img_path)
            pixel_file[i] = len(tuple_list)
            print(str(index)+" "+str(len(tuple_list)))
            index+=1




    df = pd.DataFrame(pixel_file ,columns=["ImgCollGUID","Pixel Num"])
    df.to_excel("/Users/ziweishi/Desktop/pixel_convert.xlsx")


