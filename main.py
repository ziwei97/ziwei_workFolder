import os
import shutil
import boto3
import pandas as pd
import data_validation.test_copy as ts_copy

s3 = boto3.resource('s3')


# key = "DataScience/WAUSI_SV0_0522/205-002/SV_1_Date/"
# s3.Object('spectralmd-datashare', key).delete()


structure=["PseudoColor","Assessing","Mask","Phase","Tags"]
type_list = {i:[] for i in structure}

print(type_list)