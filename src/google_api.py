from googleapiclient.discovery import build
import os.path
from datetime import datetime
import time
import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

from email.mime.text import MIMEText
import base64
from dataclasses import dataclass

# customer
from helpers import get_secret

@dataclass
class EmailData:
    From: str = None
    Subject: str = None
    Date: str = None
    Snippet: str = None
    threadId: str = None
    MessageId: str = None

    def content(self):
        content = {
            'From': self.From, 
            'Subject': self.Subject, 
            'Date': self.Date, 
            'Snippet': self.Snippet
            }
        return content
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)


    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
    
    @classmethod
    def from_object(cls, msg):
        # email data struct
        email_data = {
            'From': None,
            'Subject': None,
            'Date': None,
            'Snippet': msg['snippet'],
            'threadId': msg['threadId'],
            'MessageId': None
        }
        
        # get content from the email
        for header in msg['payload']['headers']:
            if header['name'] in email_data:
                email_data[header['name']] = header['value']

        return cls.from_dict(email_data)

SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar']
# CLIENT_SECRETS = '.secrets/creds.json'
TOKEN = '.secrets/token.json'
secret_name = "dev/google/oauth"
CLIENT_SECRETS = get_secret(secret_name)

class GoogleClient:
    def __init__(self):
        self.creds = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists(".secrets/token.json"):
            creds = Credentials.from_authorized_user_file(".secrets/token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(CLIENT_SECRETS, SCOPES)
                creds = flow.run_local_server(port=50)
            with open(".secrets/token.json", "w") as token:
                token.write(creds.to_json())
        return creds

class GmailClient(GoogleClient):
    def __init__(self):
        super().__init__()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_message(self, to, subject, message_text, thread_id=None, in_reply_to=None, user_id='reaneyassistant@gmail.com'):
        sender = user_id

        def _create_message(sender, to, subject, message_text, thread_id=None, in_reply_to=None):
            message = MIMEText(message_text)
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject

            if thread_id and in_reply_to:
                message['threadId'] = thread_id
                message['In-Reply-To'] = in_reply_to
                message['References'] = in_reply_to

            raw_message = base64.urlsafe_b64encode(message.as_bytes())
            return {'raw': raw_message.decode(), 'threadId': thread_id}
        
        message = _create_message(sender, to, subject, message_text, thread_id, in_reply_to)
        
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print(f'Message Id: {message["id"]}')
        except Exception as error:
            print(f'An error occurred: {error}')

    def check_emails(self):
        # fetch unread emails
        results = self.service.users().messages().list(userId='reaneyassistant@gmail.com', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])
        
        if not messages:
            time.sleep(1)
            self.check_emails()
        
        for message in messages:
            # get email by id
            msg = self.service.users().messages().get(userId='reaneyassistant@gmail.com', id=message['id'], format='full').execute()

            # mark unread email as read by id
            self.service.users().messages().modify(userId='reaneyassistant@gmail.com', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

            email_data = EmailData.from_object(msg)

            # save email in log
            filename = Path('.logs') / (datetime.now().strftime("%Y%m%d%H%M%S") + ".txt")
            with open(filename, 'w') as file:
                for key, value in email_data.content().items():
                    file.write(f"{key}: {value}\n")
                file.write(f"\nEmail Body:\n{msg['snippet']}\n")
            
            # print email
            print(f"Email from {email_data['From']} with subject '{email_data['Subject']}' saved to {filename}")

            # reply to email
            self.send_message(
                to=email_data.From, 
                subject=email_data.Subject, 
                message_text=f'message received! i will get right on this. \n\n response to: \n\n {email_data.Snippet}', 
                thread_id=email_data.threadId, 
                in_reply_to=email_data.MessageId)


# class CalendarClient(GoogleClient):
#     def get_calendar_service(self):
#         # Load service account credentials
#         creds = self.creds
#         # Build the Calendar service object
#         calendar_service = build('calendar', 'v3', credentials=creds)
#         return calendar_service

if __name__ == '__main__':
    logging.info('starting up service')
    client = GmailClient()
    client.check_emails()