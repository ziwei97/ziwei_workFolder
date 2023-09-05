import pandas as pd
import numpy as np

path = "/Users/ziweishi/Desktop/Book5.xlsx"

df = pd.read_excel(path)
time_list =df["time"].to_list()

year = []
month = []

m_li = ["Aug","Dec","Feb","Jul","Jun","Mar","May","Nov","Oct","Sep","Apr","Jan"]

for i in time_list:
    time_li = i.split(" ")
    if "2023" in i:
        year.append("2023")
    elif "2022" in i:
        year.append("2022")
    else:
        year.append(np.nan)

    index=0
    for h in m_li:
        index += 1
        if h in i:
            month.append(h)
            break
        else:
            if index == 12:
                month.append(np.nan)




df["year"] = year
df["month"] = month

df.to_excel("/Users/ziweishi/Desktop/time.xlsx")



