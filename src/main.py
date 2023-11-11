import logging
import os

from google_api import GmailClient
from helpers import get_secret

def main():
    # set env vars
    logging.info('setting up secrets')
    secret = get_secret('dev/tokens/helpful')
    for key, value in secret.items():
        os.environ[key] = value

    logging.info('logging into email to listen for messages')
    # load gmail client
    google_client = GmailClient()

    # listen for email commands
    while True:
        google_client.check_emails()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()