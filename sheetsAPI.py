from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.

def loginGoogle():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def runSheets(id, month, interval):
    #SAMPLE_SPREADSHEET_ID = input('Insira o endereço da tabela ')
    #SAMPLE_RANGE_NAME = 'Página1!' + input('Insira raio da tabela ')
    
    SAMPLE_SPREADSHEET_ID = id
    SAMPLE_RANGE_NAME = month+interval
    
    creds = loginGoogle()
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        
        
        return values, sheet
        
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    id = '1KfcO6J8_oLxTQIsdZ1l4XmBz-teP-pbpGoU7NnZa_KA'
    v, s = runSheets(id, 'Janeiro')
    print(v)
    
