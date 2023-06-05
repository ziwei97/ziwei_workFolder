import threading
import color_convert

if __name__ == "__main__":


    thread = 10




    pixel_file = {}
    path = "/Users/ziweishi/Desktop/WASP_Mask/"
    list = os.listdir(path)
    index = 0
    for i in list:
        if i[0] != ".":
            img_path = path + i + "/Mask_" + i + ".png"
            tuple_list = return_pixel_type(img_path)
            pixel_file[i] = len(tuple_list)
            print(str(index) + " " + str(len(tuple_list)))
            index += 1

    df = pd.DataFrame(pixel_file, columns=["ImgCollGUID", "Pixel Num"])
    df.to_excel("/Users/ziweishi/Desktop/pixel_convert.xlsx")
