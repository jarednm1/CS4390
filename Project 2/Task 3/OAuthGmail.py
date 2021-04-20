from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

#Added For Readability
TokenLocation = '/CS4390/CS4390/Project 2/Task 3/token.json'
CredentialsLocation = '/CS4390/CS4390/Project 2/Task 3/credentials.json'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TokenLocation):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CredentialsLocation, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TokenLocation, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

# Call the Gmail API
    
    emailMsg = 'Testing Gmail OAUTH - version 2 of the code'
    mimeMessage = MIMEMultipart()

# <email addr here> should be replaced with ‘user@somewhere’ 
    mimeMessage['to'] = 'jarednm@bgsu.edu'
    mimeMessage['subject'] = 'Successful Gmail OAUTH Test'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)
    

if __name__ == '__main__':
    main()