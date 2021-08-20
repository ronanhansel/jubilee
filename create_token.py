import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']
flow = InstalledAppFlow.from_client_config(
    client_config={"web":
                   {"client_id": os.getenv("client_id"),
                    "project_id": os.getenv("project_id"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": os.getenv("client_secret"),
                    }
                   }, scopes=SCOPES)
flow.redirect_uri = 'http://localhost:8080'
creds = flow.run_local_server()
# Save the credentials for the next run
with open('token.json', 'w') as token:
    token.write(creds.to_json())
print('''
    Please paste everything in token.json into an environment variable named REF_TOKEN
''')
