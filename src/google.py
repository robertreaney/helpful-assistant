from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os.path
import base64
import email
from datetime import datetime
import time
import os
import logging


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CLIENT_SECRETS_FILE = '.secrets/credentials.json'
TOKEN_FILE = '.secrest/token.json'


def get_gmail_service():
    creds = None
    # Load credentials from the token.json file if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no valid credentials available, start the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=50)  # Make sure the port matches the one in your Google API Console
        # Save the credentials for the next run to the token.json file
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Build the service object
    service = build('gmail', 'v1', credentials=creds)
    return service

def check_emails(service):
    # Call the Gmail API to fetch the inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    
    if not messages:
        time.sleep
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        
        # Use 'From', 'Subject' and 'Date' as an example, you can use other headers
        email_data = {
            'From': None,
            'Subject': None,
            'Date': None,
            'Snippet': msg['snippet']  # Email preview
        }
        
        for header in msg['payload']['headers']:
            if header['name'] in email_data:
                email_data[header['name']] = header['value']
        
        # Save the email content to a file
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
        with open(filename, 'w') as file:
            for key, value in email_data.items():
                file.write(f"{key}: {value}\n")
            file.write(f"\nEmail Body:\n{msg['snippet']}\n")
        
        print(f"Email from {email_data['From']} with subject '{email_data['Subject']}' saved to {filename}")

if __name__ == '__main__':
    service = get_gmail_service()
    check_emails(service)