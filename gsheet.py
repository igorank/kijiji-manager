import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_gs_client(key, keyfile_name):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(str(keyfile_name), scope)
    auth = gspread.authorize(credentials)
    client = auth.open_by_key(str(key))
    return client


def get_empty_row_in_col(worksheet, col_num):
    return len(worksheet.col_values(col_num)) + 1


class GSheet:

    def __init__(self, key, keyfile_name):
        self.gs_client = get_gs_client(key, keyfile_name)

    def get_main_worksheet(self, worksheet_id):
        return self.gs_client.get_worksheet_by_id(int(worksheet_id))

    def get_leads_worksheet(self, worksheet_id):
        return self.gs_client.get_worksheet_by_id(int(worksheet_id))
