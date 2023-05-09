import pandas as pd
import os
import json

# df = pd.read_excel("/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.csv")

path = '/Users/ziweishi/Downloads/database_json/'
path = os.path.expanduser(path)
file = "ePOC_ImageCollection.json"
df = pd.read_json((path+file), lines=True, dtype=False)

df.to_csv("/Users/ziweishi/Downloads/final.csv")

print(len(df))

corpous = [{"name":"apple","type":"iphone11"},{"name":"huawei","type":"rongyao","battery":"90%"}]


# new_file = json.loads(corpous)

with open('/Users/ziweishi/Downloads/database_json/practice.json','w') as json_file:
    for each_dict in corpous:
        json_file.write(json.dumps(each_dict)+'\n')


l = "/Users/ziweishi/Downloads/database_json/practice.json"
path = os.path.expanduser(l)
df = pd.read_json(path, lines=True, dtype=False)
df.to_csv("/Users/ziweishi/Downloads/database_json/practice.csv")
print(df)
