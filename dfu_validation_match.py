import transfer_check
import pandas as pd


a = input("refresh db?")

if a =="yes":
    db = transfer_check.output_total()
else:
    db = pd.read_excel("/Users/ziweishi/Desktop/dfu_check.xlsx")


