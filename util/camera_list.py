import pandas as pd

df = pd.read_csv("/Users/ziweishi/Documents/database/BURN_Master_ImageCollections.csv")
df = df[["Site","Raw"]]
df=df[df["Raw"].notna()]



raw = df["Raw"].to_list()
site = df["Site"].to_list()

camera_id = []
photo_index=[]
site_id = []

a = len(raw)

for i in range(a):
    raw_text = raw[i]
    if raw_text[2:5] == "Raw":
        raw_list = raw_text.split(",")
        for x in raw_list:
            info= x.split("_")
            if len(info)>3:
                site_id.append(site[i])
                camera_name = info[2]
                # index = info[1]
                # photo_index.append(index)
                camera_id.append(camera_name)


final=zip(site_id,camera_id)
final_data = pd.DataFrame(final,columns=["site","cameraID"])

final_data.drop_duplicates()

final_data.to_csv("/Users/ziweishi/Documents/database/Camera_List.csv")