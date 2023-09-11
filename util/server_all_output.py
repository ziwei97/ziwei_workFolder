import dfu.transfer_check as transfer_check
import pandas as pd

def output_total():
    a = input("new output?")
    if a =="yes":
        check_site = ["nynw", "ocer", "whfa", "youngst", "lvrpool", "memdfu", "hilloh", "grovoh", "mentoh",
                      "encinogho", "lahdfu", "rsci"]
        site_list = transfer_check.refresh_sql_database(check_site)
        if site_list != False:
            check_list = {}
            for check in check_site:
                check_list[check] = site_list[check]
            data_sites = []
            for i in check_list.keys():
                path = check_list[i]["sql_path"]
                df_guid, df_image, site, check_path = transfer_check.server_table_output(path, i)
                data_sites.append(df_guid)
            union_df = pd.concat(data_sites)
            union_df.to_excel("../Documents/dfu_all.xlsx")
            return union_df
        else:
            print("Wrong Path!")
    else:
        df = pd.read_excel("../Documents/dfu_all.xlsx")
        return df