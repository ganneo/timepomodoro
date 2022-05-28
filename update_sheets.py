import json
import os
import urllib.parse
from pathlib import Path
from constant import SECRET_FILE
import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials


def write_credential():
    """
    read from environment variable and write to credential file, which is git ignored
    :return: None
    """
    credential_dict = dict()
    credential_dict["project_id"] = os.getenv("POMODORO_PROJECT_ID")
    credential_dict["private_key_id"] = os.getenv("POMODORO_KEY_ID")
    credential_dict["private_key"] = os.getenv("POMODORO_KEY")
    credential_dict["client_email"] = os.getenv("POMODORO_EMAIL")
    credential_dict["client_id"] = os.getenv("POMODORO_CLIENT_ID")
    credential_dict["type"] = "service_account"
    credential_dict["auth_uri"] = "https://accounts.google.com/o/oauth2/auth"
    credential_dict["token_uri"] = "https://oauth2.googleapis.com/token"
    credential_dict["auth_provider_x509_cert_url"] = "https://www.googleapis.com/oauth2/v1/certs"
    credential_dict["client_x509_cert_url"] = "https://www.googleapis.com/robot/v1/metadata/x509/" + urllib.parse.quote(
        credential_dict["client_email"])
    with open(SECRET_FILE, "w") as f:
        json.dump(credential_dict, f)


def get_next_row(spread_sheet: Worksheet):
    return len(list(filter(None, spread_sheet.col_values(1)))) + 1


def add_to_raw_data(activity, start_time, end_time):
    # setup the credential file
    credential_file = Path(SECRET_FILE)
    if not credential_file.exists():
        write_credential()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRET_FILE, scope)
    client = gspread.authorize(credentials)
    raw_data_sheet = client.open_by_url(os.getenv("POMODORO_GSHEET_URL")).get_worksheet(0)

    index = get_next_row(raw_data_sheet)
    raw_data_sheet.update(f"A{index}", [[activity]])
    raw_data_sheet.update(f"B{index}", [[start_time]])
    raw_data_sheet.update(f"C{index}", [[end_time]])
