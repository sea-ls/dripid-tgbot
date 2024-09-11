import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config


def get_google_api():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.SERVICE, scope)
    client = gspread.authorize(credentials)

    # Открываем таблицу по ее названию
    spreadsheet = client.open_by_key(config.TABLE_ID)

    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
    return data