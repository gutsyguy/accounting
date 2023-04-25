from flask import Flask
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of the target Google Drive folder where the new spreadsheet will be created
TARGET_FOLDER_ID = os.environ.get("TARGET_FOLDER_ID")


def create_spreadsheet():
    """Creates a new spreadsheet in Google Sheets and returns its ID"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Create a new spreadsheet with a specific name in the target folder
        spreadsheet_name = "New Spreadsheet"
        body = {
            "parents": [TARGET_FOLDER_ID],
            "properties": {"title": spreadsheet_name},
        }
        spreadsheet = service.spreadsheets().create(body=body).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        return spreadsheet_id
    except HttpError as err:
        print(err)


@app.route('/')
def create_sheet():
    spreadsheet_id = create_spreadsheet()
    return f"New Spreadsheet created with ID: {spreadsheet_id}"


if __name__ == '__main__':
    app.run()
