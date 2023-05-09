import pandas as pd
import boto3

data = pd.read_csv("/Users/ziweishi/Downloads/corey_guid.csv")

list = data["GUID"].to_list()
# burnNum_pat_loc, BurnIndex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BURN_Master_ImageCollections')
# site = []
# DeviceType = []
# ImageCollTime = []
# ImageCollectionID = []
# JsonFileName = []
# burnindex=[]
# subjectid = []
# burnNum_pat_loc = []

SubjectID = []
PrimaryDoctorTruth = []
SecondaryDoctorTruth = []
FinalTruth = []

Status=[]

Tags = []



import datetime

for i in list:
    response = table.get_item(
        Key={
            'ImgCollGUID': i
        }
    )
    try:
        SubjectID.append(response["Item"]["SubjectID"])
    except:
        SubjectID.append("N")


    try:
        PrimaryDoctorTruth.append(response["Item"]["PrimaryDoctorTruth"])
    except:
        PrimaryDoctorTruth.append("N")

    try:
        SecondaryDoctorTruth.append(response["Item"]["SecondaryDoctorTruth"])
    except:
        SecondaryDoctorTruth.append("N")

    try:
        FinalTruth.append(response["Item"]["FinalTruth"])
    except:
        FinalTruth.append("N")
    try:
        Status.append(response["Item"]["Status"])
    except:
        Status.append("N")

    try:
        Tags.append(response["Item"]["Tags"])
    except:
        Tags.append("N")


    # try:
    #     site.append(response["Item"]["Site"])
    #
    # except:
    #     site.append(" ")
    #
    # try:
    #     DeviceType.append(response["Item"]["DeviceType"])
    # except:
    #     DeviceType.append(" ")
    #
    # try:
    #     date1 = response["Item"]["CaptureDate"]
    #     date_string = datetime.datetime.year(date1)+'-'+datetime.datetime.month(date1)+'-'+datetime.datetime.day(date1)
    #     date_time_string = datetime.datetime.hour(date1)+'.'+datetime.datetime.minute(date1)+'.'+datetime.datetime.second(date1)
    #     string_time = date_string+'_'+date_time_string
    #     ImageCollTime.append(string_time)
    # except:
    #     raw = str(response["Item"]["Raw"])
    #     final = raw.replace('[','').replace(']','').split(',')
    #     final = sorted(final)
    #
    #     p = final[0][-29:-10]
    #
    #     ImageCollTime.append(p)
    #
    # # try:
    # #     ImageCollectionID.append(response["Item"]["ImageCollectionID"])
    # # except:
    # #     ImageCollectionID.append(" ")
    #
    # try:
    #     JsonFileName.append(response["Item"]["JsonFileName"])
    # except:
    #     JsonFileName.append(" ")
    #
    # try:
    #     burnindex.append(response["Item"]["Wound"])
    # except:
    #     burnindex.append(" ")
    #
    # try:
    #     subjectid.append(response["Item"]["SubjectID"])
    # except:
    #
    #     subjectid.append(" ")
    #
    # try:
    #     burnnum=response["Item"]["SubjectID"]
    #     pat = response["Item"]["AnatomicalLocation"]
    #     wound = response["Item"]["Wound"]
    #     loc = response["Item"]["DeviceType"]
    #     burnNum_pat_loc_1 = "('"+burnnum+"','"+pat+"','"+wound+"','"+loc+"')"
    #     burnNum_pat_loc.append(burnNum_pat_loc_1)
    # except:
    #     burnNum_pat_loc.append(' ')


# print(site)
# print(DeviceType)
# print(ImageCollTime)
# print(ImageCollectionID)

# print(len(site))
# print(len(DeviceType))
# print(len(ImageCollTime))
# print(len(ImageCollectionID))
# print(len(JsonFileName))



# final =pd.DataFrame()
# final['ImgCollGUID']=list
# final['Site']=site
# final['DeviceType']=DeviceType
# final['ImageCollTime']=ImageCollTime
# final['ImageCollectionID']=ImageCollectionID
# final['JsonFileName'] = JsonFileName

# JsonFile = []
#
# for c in JsonFileName:
#     c1 = c + ".json"
#     JsonFile.append(c1)

print(len(SubjectID))

data_tuples = zip(list,SubjectID,PrimaryDoctorTruth,SecondaryDoctorTruth,FinalTruth,Tags,Status)
final = pd.DataFrame(data_tuples, columns=['Guid','SubjectID','PrimaryDoctorTruth','SecondaryDoctorTruth','FinalTruth','Tags','Status'])
final.to_csv("//Users/ziweishi/Documents/final.csv",encoding='utf-8')
# datatime = []