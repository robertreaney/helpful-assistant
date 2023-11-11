import logging

from google_api import GmailClient

def main():
    google_client = GmailClient()

    while True:
        google_client.check_emails()

if __name__ == '__main__':
    main()