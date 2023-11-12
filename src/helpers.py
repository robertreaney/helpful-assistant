# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
import json

class ListFile:
    bucket_name = 'reaney-helpfulai'
    file_name = 'list.txt'

    def __init__(self):
        self.s3 = boto3.client('s3')
        try:
            self.file = self.s3.get_object(Bucket=self.bucket_name, Key=self.file_name)
            self.content = self.file['Body'].read().decode('utf-8')
        except:
            pass

    def write(self, content):
        self.s3.put_object(Bucket=self.bucket_name, Key=self.file_name, Body=content)


def get_secret(secret_name, region_name='us-east-1'):

    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.
    return json.loads(secret)
