import pandas as pd

data = pd.read_excel("/Users/ziweishi/Desktop/Book1.xlsx")

list = data.columns

# for i in list:
#     print(i)

select_col = ["Participant Id","BSV_date"]

for j in range(2,13):
    col = "SV"+str(j)+"_SV_date"
    select_col.append(col)

print(select_col)

final = data[select_col]

print(final.head(5))



count_num  = final.count(axis='columns')
print(count_num)






