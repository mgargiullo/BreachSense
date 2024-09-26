import boto3
from botocore.exceptions import ClientError
import json
import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def get_secret():

    secret_name = "Breachsense_API_Key"
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

    secret_json_txt = get_secret_value_response['SecretString']
    secret_json = json.loads(secret_json_txt)

    return secret_json['BS_API_KEY']