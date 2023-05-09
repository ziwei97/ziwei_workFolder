import os
import pandas as pd
import download_whole_dynamodb_table



df = download_whole_dynamodb_table.get_table('BURN_Master_ImageCollections')


column = ["ImgCollGUID","SubjectID","AnatomicalLocation","Suffix","Wound","Tags","Status","Site","StudyName","Bucket"]
df3 = df.loc[:,column]

df4 = df3[df3["StudyName"]=="BURN_BTS"]
df4.to_excel('/Users/ziweishi/Documents/server_check/BURN_summary.xlsx')


def replace_all(site,patient_id):

    if site == "yalebridgeport":
        list = ["_1008", "_108"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")

        patient_id=patient_id.replace("Patient_","108-")

    if site == "medstardc":
        list = ["_108"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_018")
        patient_id=patient_id.replace("Patient_", "103-")

    if site == "unialab":
        list = ["_105"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_", "105-")

    if site == "chnola":
        list = ["_106"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i,"_")
        patient_id=patient_id.replace("Patient_", "106-")

    if site == "nolaepoc":
        list = ["_9105","_9106","_9107"]
        for i in list:
            p = "_00"+i[-1]
            if i in patient_id:
                patient_id=patient_id.replace(i, p)
                patient_id=patient_id.replace("Patient_","106-")

        patient_id=patient_id.replace("Patient_", "101-")

    if site == "wakeforest":
        list = ["_102"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_")

        patient_id=patient_id.replace("Patient_", "102-")

    if site == "medunisc":
        if "_001" in patient_id:
            patient_id=patient_id.replace("_001", "_9999")

        list = ["_100"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_00")

        patient_id=patient_id.replace("Patient_", "107-")

    if site == "phxvw":
        list = ["_109"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_")

        patient_id=patient_id.replace("Patient_", "109-")

    if site == "massgho":
        list = ["_0001"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_001")

        patient_id=patient_id.replace("Patient_", "104-")

    if site == "chphil":
        list = ["_111"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_")
        if "_02" in patient_id:
            patient_id=patient_id.replace("_02","_002")
        patient_id=patient_id.replace("Patient_", "111-")

    if site == "nysb":
        list = ["_110"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_")

        patient_id=patient_id.replace("Patient_", "110-")

    if site == "chmedunisc":
        list = ["_1001"]
        for i in list:
            if i in patient_id:
                patient_id=patient_id.replace(i, "_9999")

        patient_id=patient_id.replace("Patient_", "107-")

    return patient_id

bucket_corpus="""yalebridgeport
medstardc
unialab
chnola
nolaepoc
wakeforest
medunisc
phxvw
massgho
chphil
nysb
chmedunisc"""

bucket_list = bucket_corpus.split("\n")



site = []
device = []
patient_list = []
location_list=[]
suffix_list=[]
filter_file_list = []



for i in bucket_list:
    path = "/Volumes/epoc/DataTransfers/"
    folder_path = os.path.join(path, i)
    burn_path = os.path.join(folder_path,"BURN_BTS")
    device_id_list = os.listdir(burn_path)


    for j in device_id_list:
        if j[0:3]== 'SMD':
            device_path = os.path.join(burn_path,j)
            patient_path =os.path.join(device_path,"SpectralView/Burn")
            patients = os.listdir(patient_path)
            for p in patients:
                if p[0] != ".":
                    patient_id = replace_all(i, p)
                    patient_check = (patient_id.split("-"))[1]
                    test_id = ["000", "0000", "998", "9999", "8888", "111111", "999", "9876", "9998"]
                    if patient_check not in test_id:
                        injury = p + "/Injury_1/"
                        location_path = os.path.join(patient_path, injury)
                        locations = os.listdir(location_path)
                        for q in locations:
                            if q[0] != ".":
                                suffix_path = os.path.join(location_path, q)
                                suffixs = os.listdir(suffix_path)
                                for x in suffixs:
                                    if x[0] != ".":
                                        collection_path = os.path.join(suffix_path, x)
                                        collections = os.listdir(collection_path)
                                        for y in collections:
                                            if y[0] != ".":
                                                filter_file_list.append(y)
                                                suffix_list.append(x)
                                                location_list.append(q)
                                                patient_list.append(patient_id)
                                                device.append(j)
                                                site.append(i)


data = zip(site,device,patient_list,location_list,suffix_list,filter_file_list)
server_final = pd.DataFrame(data, columns=["Site","Device","SubjectID","Location","Suffix","Collection_file"])
server_final.to_excel("/Users/ziweishi/Documents/server_check/Step_1_Server_Collection_checking.xlsx")

print("Step 1 Finished")


patient_site = []
patient_final_list = []
patient_final_num = []

for x in bucket_list:
    server_final1 = server_final[server_final["Site"]==x]
    patient_list1 = server_final1["SubjectID"].to_list()
    patient_num = {}

    for i in patient_list1:
        if i not in patient_num:
            patient_num[i] = 1
        else:
            patient_num[i] += 1

    for j in patient_num:
        patient_site.append(x)
        patient_final_list.append(j)
        a = patient_num[j]
        patient_final_num.append(a)


patient_data = zip(patient_site,patient_final_list,patient_final_num)
patient_final =pd.DataFrame(patient_data,columns = ['Site','PatientID','Collection_Nums'])
patient_final.to_excel("/Users/ziweishi/Documents/server_check/Step_2_Server_Patient_num.xlsx")


print("Step 2 Finished")



df_db = pd.read_excel("/Users/ziweishi/Documents/server_check/BURN_summary.xlsx")
db_site = []
db_final_list = []
db_final_num = []
for x in bucket_list:
    df_db1 = df_db[df_db["Bucket"]==x]
    patient_list = df_db1["SubjectID"].to_list()
    patient_num = {}

    for i in patient_list:
        if i not in patient_num:
            patient_num[i] = 1
        else:
            patient_num[i] += 1

    for j in patient_num:
        db_site.append(x)
        db_final_list.append(j)
        a = patient_num[j]
        db_final_num.append(a)

db_data = zip(db_site,db_final_list,db_final_num)
# patient_final = pd.DataFrame(list(patient_num.items()),columns = ['PatientID','Collection_Nums'])
db_final =pd.DataFrame(db_data,columns = ['Site','PatientID','Collection_Nums'])
db_final.to_excel("/Users/ziweishi/Documents/server_check/Step_3_db_Patient_num.xlsx")

print("Step 3 Finished")


diff_buck = []
diff_sub = []
ser_num = []
dbb_num=[]
diff_num = []


for w in bucket_list:

    pf1 = patient_final[patient_final["Site"]==w]
    db1 = db_final[db_final["Site"]==w]
    subjects = pf1["PatientID"].to_list()

    for g in subjects:
        if g not in ["105-46" ,"105-050","106-005","106-006","106-007","105-002","105-003","105-046","105-040","102-022"]:
            pf2 = pf1[pf1["PatientID"] == g]
            server_num = pf2["Collection_Nums"].iloc[0]
            db2 = db1[db1["PatientID"] == g]
            db_num = db2["Collection_Nums"].iloc[0]
            if server_num != db_num:
                diff_buck.append(w)
                diff_sub.append(g)
                ser_num.append(server_num)
                dbb_num.append(db_num)
                diff_num.append(str(server_num-db_num))



diff_data = zip(diff_buck,diff_sub,ser_num,dbb_num,diff_num)
diff_final =pd.DataFrame(diff_data,columns = ['Site','PatientID','Server_Num','DB_Num','Diff_Collection_Nums'])
diff_final.to_excel("/Users/ziweishi/Documents/server_check/Step_4_diff_Patient_num.xlsx")

print("Step 4 Finished")
