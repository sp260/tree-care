from google.auth import app_engine
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = '1OUoRgrOKsIydUpwdFxyY8B2rUVg7EdA3HsbqSKVQZeY'
SERVICE_ACCOUNT_PATH_JSON = 'tree-care-241710-4e10da4f25af.json'

def auth_sheets_api():
    """
    authentification in sheets api
    :return: service
    """
    # Check environment
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Production
        credentials = app_engine.Credentials(scopes=SCOPES)
    else:
        # Local development server
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH_JSON)

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_volunteers():
    """
    get new volunteers from sheet
    :return:
    """
    service = auth_sheets_api()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='A2:F').execute()
    values = result.get('values', [])
    new_volunteers = []
    for i, row in enumerate(values):
        if len(row) == 6 and row[5] == 'oui':
            new_volunteers.append((i+2, row[:5]))
    return new_volunteers

def insert_row(request):
    """
    :param request:
    :return:
    """
    service = auth_sheets_api()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='A2:E').execute()
    values = result.get('values', [])
    range = 'A' + str(len(values)+2)

    volunteer = [
        request.get('last_name'), 
        request.get('first_name'), 
        request.get('adress'), 
        request.get('email'), 
        request.get('id_tree')
    ]

    value_range_body = {
        'values': [volunteer]
    }

    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                                    body=value_range_body, valueInputOption='RAW')
    response = request.execute()

def update_row(num_range):
    """
    update data in sheet
    :return:
    """
    service = auth_sheets_api()    
    sheet = service.spreadsheets()
    value_range_body = {
        'values': [['ok']]
    }
    range = 'G' + str(num_range)
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                                    body=value_range_body, valueInputOption='RAW')
    response = request.execute()

def clear_data(range):
    """
    :param range:
    :return:
    """
    service = auth_sheets_api()   
    sheet = service.spreadsheets()
    request = sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=range)
    response = request.execute()