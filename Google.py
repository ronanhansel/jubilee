import pickle
import json
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def create_service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created when the authorization flow completes for the first
    # time.
    try:
        creds = Credentials.from_authorized_user_info(
            info=json.loads(os.getenv('REF_TOKEN')), scopes=SCOPES)
    except Exception:
        raise AttributeError(
            '''Try running the create_token.py script, it'll output token.json including all required credentials, copy and paste it to the environment variables with key: REF_TOKEN''')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid or creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            raise AttributeError('''Try running the create_token.py script, 
        it'll out put your token.json including all required credentials, copy and paste it to the environment variables with key: REF_TOKEN''')
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
