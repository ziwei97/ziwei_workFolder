import os
import pandas as pd

path = "/Volumes/epoc/DataTransfers/unialab/UNIALAB_BURN_SMD2138-013_09_25_23/SpectralView"


guid=[]
file=[]


def all_file_list(path):

    check_list = os.listdir(path)
    if ".DS_Store" in check_list:
        check_list.remove(".DS_Store")
    for i in check_list:
        path_new = os.path.join(path, i)
        # path_latest = os.path.join(path_new,"MSI")
        list_new = os.listdir(path_new)
        if ".DS_Store" in list_new:
            list_new.remove(".DS_Store")
        for j in list_new:
            guid.append(i)
            file.append(j)

folders = 0

def print_files(path,list):
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(
        path, i))]
    global folders
    if dirs:
        for i in dirs:
            folders += 1
            print_files(os.path.join(path, i),list)
    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    for f in files:
        a = str(f).split("/")
        b= a[-1]
        # list.append(os.path.join(path, f))
        list.append(f)
    return list,folders

a = []

result = print_files(path,a)
list_file=result[0]
num = result[1]
print(num)






final = pd.DataFrame(list_file,columns=["file"])
final.to_excel("/Users/ziweishi/Desktop/final_list.xlsx")

