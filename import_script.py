import pandas as pd
import os
import json
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# if os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"):
#     service_account_info = json.loads(
#         os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
#     )

#     credentials = Credentials.from_service_account_info(
#         service_account_info,
#         scopes=SCOPES
#     )

credentials = Credentials.from_service_account_file(
    r"D:\swalih\resource_search\credentials\dash-analysis-503210-5b2081c42f52.json",
    scopes = SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open("Du SFAN-Database! V2")

def getResourceSheet():
    return spreadsheet.worksheet('Current')