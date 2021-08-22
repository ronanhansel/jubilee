from google import create_service
import os

CLIENT_SECRET = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
DEFAULT_ID = os.getenv('DRIVE_DEFAULT_ID')
service = create_service(CLIENT_SECRET, API_NAME, API_VERSION, SCOPES)


def create(folder):
    folders = folder.split("/")
    folder_id = ''
    default_id = DEFAULT_ID
    for i in folders:
        if folder_id == '':
            folder_id = default_id
        if i[0] == '&':
            a = i[1:].split("..")
            for e in a:
                file_metadata = {
                    'name': e,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [folder_id]
                }
                service.files().create(body=file_metadata,
                                       supportsAllDrives=True, fields='id').execute()
            return
        else:
            file_metadata = {
                'name': i,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder_id]
            }
            file = service.files().create(body=file_metadata,
                                          supportsAllDrives=True, fields='id').execute()

            folder_id = file.get('id')
