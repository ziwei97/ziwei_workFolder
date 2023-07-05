import json
from turtle import left
import pandas as pd
from typing import List, Dict

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

WAUSI_STUDY_ID = "5FACAEE8-CF5F-4FE4-8E3B-1D27E0780837"
WOUND_MAP_SUFFIX = {
    "0": "Forefoot",
    "1": "Midfoot",
    "2": "Hindfoot",
    "5": "1st_Toe",
    "6": "2nd_Toe",
    "7": "3rd_Toe",
    "8": "4th_Toe",
    "9": "5th_Toe"
}
WOUND_MAP_PREFIX = {
    "0": "Left",
    "1": "Right"
}


def auth():
    Client_ID = "57F3AC02-E882-44BB-B4F5-2EACC9B08FCF"
    Client_Secret = "dd5001cd2f3d3c57b1233d3c1427c4a7"

    token_post = "https://us.castoredc.com/oauth/token"
    auth = HTTPBasicAuth(Client_ID, Client_Secret)
    client = BackendApplicationClient(client_id=Client_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_post, auth=auth)
    access_token = token["access_token"]

    return {"Authorization": "Bearer %s" % access_token}


def add_visit_times(parsed_subjects: List[Dict]) -> List[Dict]:
    base = "https://us.castoredc.com/api"
    append_data = []
    for subject in parsed_subjects:

        subjects_data__endpoint = f'{base}/study/{WAUSI_STUDY_ID}/participant/{subject.get("SubjectID")}/data-point/study?page_size=1000'
        data_response = requests.get(subjects_data__endpoint, headers=auth())
        datapoints_raw = data_response.json().get("_embedded").get("StudyDataPoints")
        while data_response.json()['page'] != data_response.json()['page_count']:
            data_response = requests.get(data_response.json()['_links']["next"]['href'], headers=auth())
            datapoints_raw.extend(data_response.json().get("_embedded").get("StudyDataPoints"))

        flat_datapoints = {}
        for datapoint in datapoints_raw:
            visit_field = {
                datapoint.get("field_variable_name"): datapoint.get("value")
            }
            flat_datapoints = flat_datapoints | visit_field

        parsed_fields = {
            "EOS Date": flat_datapoints.get("EOS_date", ''),
            "SV_1_Date": flat_datapoints.get("BSV_date", ''),
            # "SV_1_Occur": 'Yes' if flat_datapoints.get("SV_Occur_1", '') == '0' else 'No',
            "SV_2_Date": flat_datapoints.get("SV2_SV_date", ''),
            # "SV_2_Occur": 'Yes' if flat_datapoints.get("SV_Occur_2", '') == '0' else 'No',
            "SV_3_Date": flat_datapoints.get("SV3_SV_date", ''),
            # "SV_3_Occur":  'Yes' if flat_datapoints.get("SV_Occur_3", '') == '0' else 'No',
            "SV_4_Date": flat_datapoints.get("SV4_SV_date", ''),
            # "SV_4_Occur":  'Yes' if flat_datapoints.get("SV_Occur_4", '') == '0' else 'No',
            "SV_5_Date": flat_datapoints.get("SV5_SV_date", ''),
            # "SV_5_Occur":  'Yes' if flat_datapoints.get("SV_Occur_5", '') == '0' else 'No',
            "SV_6_Date": flat_datapoints.get("SV6_SV_date", ''),
            # "SV_6_Occur":  'Yes' if flat_datapoints.get("SV_Occur_6", '') == '0' else 'No',
            "SV_7_Date": flat_datapoints.get("SV7_SV_date", ''),
            # "SV_7_Occur":  'Yes' if flat_datapoints.get("SV_Occur_7", '') == '0' else 'No',
            "SV_8_Date": flat_datapoints.get("SV8_SV_date", ''),
            # "SV_8_Occur":  'Yes' if flat_datapoints.get("SV_Occur_8", '') == '0' else 'No',
            "SV_9_Date": flat_datapoints.get("SV9_SV_date", ''),
            # "SV_9_Occur": 'Yes' if flat_datapoints.get("SV_Occur_9", '') == '0' else 'No',
            "SV_10_Date": flat_datapoints.get("SV10_SV_date", ''),
            # "SV_10_Occur": 'Yes' if flat_datapoints.get("SV_Occur_10", '') == '0' else 'No',
            "SV_11_Date": flat_datapoints.get("SV11_SV_date", ''),
            # "SV_11_Occur": 'Yes' if flat_datapoints.get("SV_Occur_11", '') == '0' else 'No',
            "SV_12_Date": flat_datapoints.get("SV12_SV_date", ''),
            # "SV_12_Occur": 'Yes' if flat_datapoints.get("SV_Occur_12", '') == '0' else 'No',
        }
        subject = subject | parsed_fields
        append_data.append(subject)
    return append_data


def get_patient_data() -> List[Dict]:
    ############
    ## URLS for Future USE
    ############

    # LOAD LOCAL DATA FOR TESTING
    # response_file = open('participant_api_sample.json')
    # raw_participants = json.load(response_file)
    # response_file.close()

    base = "https://us.castoredc.com/api"
    subjects_endpoint = f'{base}/study/{WAUSI_STUDY_ID}/participant?page_size=1000'

    # print(f'{" Retrieving Subjects Data From Castor ":#^50}')
    data_response = requests.get(subjects_endpoint, headers=auth())
    raw_participants: List[Dict] = data_response.json()['_embedded']["participants"]
    while data_response.json()['page'] != data_response.json()['page_count']:
        data_response = requests.get(data_response.json()['_links']["next"]['href'], headers=auth())
        raw_participants.extend(data_response.json()['_embedded']["participants"])

    print(f'{" Parsing Data ":#^50}')

    parsed_subject_data = []
    for subject in raw_participants:
        parsed_subject = {
            "SubjectID": subject.get('id'),
            'Progress': subject.get('progress'),
            "Status": subject.get('status'),
            'Archived': subject.get('archived'),
            'ArchivedReason': subject.get('archived_reason'),
            "SiteName": subject.get('_embedded', '').get('site').get('name'),
            "SiteAbv": subject.get('_embedded', '').get('site').get('abbreviation'),
            "SiteID": subject.get('_embedded', '').get('site').get('code'),
            "SiteCastorID": subject.get('_embedded', '').get('site').get('id')
        }
        parsed_subject_data.append(parsed_subject)
    print(f'{" Complete ":#^50}')
    return parsed_subject_data


def add_wound_location(subject_data) -> List[Dict]:
    base = "https://us.castoredc.com/api"
    append_data = []

    # print(f'{" Retrieving Wound Data From Castor ":#^50}')
    for subject in subject_data:
        subjects_data__endpoint = f'{base}/study/{WAUSI_STUDY_ID}/participant/{subject.get("SubjectID")}/data-point/study?page_size=1000'
        data_response = requests.get(subjects_data__endpoint, headers=auth())
        datapoints_raw = data_response.json().get("_embedded").get("StudyDataPoints")
        while data_response.json()['page'] != data_response.json()['page_count']:
            data_response = requests.get(data_response.json()['_links']["next"]['href'], headers=auth())
            datapoints_raw.extend(data_response.json().get("_embedded").get("StudyDataPoints"))

        flat_datapoints = {}
        for datapoint in datapoints_raw:
            visit_field = {
                datapoint.get("field_variable_name"): datapoint.get("value")
            }
            flat_datapoints = flat_datapoints | visit_field

        prefix = WOUND_MAP_PREFIX.get(flat_datapoints.get("left_right"), '')
        suffix = WOUND_MAP_SUFFIX.get(flat_datapoints.get("dfu_position"), '')

        parsed_fields = {
            "CastorAnatomicalLocation": f'{prefix}_{suffix}'
        }
        subject = subject | parsed_fields
        append_data.append(subject)
        append_data.append(subject)
    print(f'{"Data Complete":#^50}')
    return append_data


def main():
    subject_data = get_patient_data()
    wound_data = add_wound_location(subject_data)
    pd.DataFrame(wound_data).to_excel("Wound_Data.xlsx")
    visit_data = add_visit_times(subject_data)
    pd.DataFrame(visit_data).to_excel("Visit_Data.xlsx")


if __name__ == "__main__":
    main()
