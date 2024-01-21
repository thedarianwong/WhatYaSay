import os.path
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials 



SCOPES = ['https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/docs',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.metadata.readonly']

def request_creds() :
    creds = None 
    if os.path.exists('creds.json'):
        flow = InstalledAppFlow.from_client_secrets_file('creds.json', SCOPES)
        creds = flow.run_local_server(part=0)
        with open ('token.json','w') as token:
            token.write(creds.to_json())
        return Credentials.from_authorized_user_file('token.json', SCOPES)  
    else:
        print('Credentials not present')
        sys.exit(1) 