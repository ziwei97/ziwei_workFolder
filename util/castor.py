import pandas as pd
#
df = pd.read_excel("/Users/ziweishi/Desktop/Truthing_List.xlsx",sheet_name="total")

id = df["Subject"].to_list()
# list = pd.read_excel("/Users/ziweishi/Desktop/ImageData_DecemberTruthing.xlsx",sheet_name="December-Truth-Data")
#
# sub_list = list["SubjectID"].to_list()
# df1 = df[df["D_sub_num"].isin(sub_list)]
# df1.to_excel("/Users/ziweishi/Desktop/new.xlsx")


# a = df1[df1["D_sub_num"]=="101-001"]
#
# for i in sub_list[1:]:
#     try:
#         df2=df1[df1["D_sub_num"]==i]
#         new = [a,df2]
#         a = pd.concat(new)
#     except:
#         print(i)
#         df2 = df1[df1["D_sub_num"] == "108-004"]
#         new = [a, df2]
#         a = pd.concat(new)
#
#
# a.to_excel("/Users/ziweishi/Desktop/try.xlsx")



def find_duplicate(list):
    index = {}
    a = 0
    for i in list:
        index[a]=[]
        b=a+1
        for j in list[b:]:
            if i==j:
                index[a].append(b)
            b+=1
        a+=1
    return index


def remove_duplicate(list):
    index=find_duplicate(list)
    duplicate = []
    for i in index:
        extra = index[i]
        for j in extra:
            if j not in duplicate:
                duplicate.append(j)
    a=0
    final = []
    for s in list:
        if a not in duplicate:
            final.append(s)
        a+=1
    return final

a = remove_duplicate(id)
print(len(a))
# for i in range(len(a)):
#     print(a[i])

# list1 = [2,3,4,1,2,3,5]
# print(remove_duplicate(list1))

# ch1 = remove_duplicate(ch)
# pei1 = remove_duplicate(pei)
# pei2 = []
# for i in pei1:
#     if i[0] != '0':
#         pei2.append(i)
# print(len(ch1))
# print(len(pei2))
#
# for i in ch1:
#     if i not in pei2:
#         print(i)

#
# excel_file_path = '/Users/ziweishi/Desktop/Training_Study_excel_export_20221122021018.xlsx'
# df = pd.read_excel(excel_file_path, sheet_name=1)
#
# columns = ['Accession#', 'Location#', 'SubjectID', 'StudyID', 'BiopsyID', 'Location', 'R.L', 'Site', 'Other',
# 'PERCENT >50%', 'Viable Papillary Dermis', 'Reticular Dermis', 'DEGENERATION OF RETICULAR DERMIS COLLAGEN',
# 'Total # of Necrotic & Viable', 'Total # of Necrotic Only', 'DEGREE OF THROMBOSIS']



# new_df = pd.DataFrame(df.values, columns = columns)

# new_df.to_csv('/Users/ziweishi/Desktop/use.csv')


