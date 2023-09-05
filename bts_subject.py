import os
import shutil
import boto3
import numpy as np
import pandas as pd
import data_validation.test_copy as ts_copy
import util.update_attr as update

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

table_name = 'BURN_Master_ImageCollections'
table = dynamodb.Table(table_name)

