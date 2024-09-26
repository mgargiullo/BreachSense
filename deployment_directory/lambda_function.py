import json
import os
import requests
import boto3
from botocore.exceptions import ClientError


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

    secret = get_secret_value_response['SecretString']
    return secret

def lambda_handler(event, context):
    API_KEY = get_secret()
    API_URL = os.environ.get('BS_API_URL')
    PARAMS = {'lic': API_KEY, 's': event['search_string'], 'attr': True}
    req = requests.get(API_URL, params=PARAMS)
    returned_data = json.loads(req.text)
    tmp_dict = dict()
    for item in returned_data:
        email = item['eml']
        src = item['src']
        key = ''.join(e for e in src if e.isalnum())
        pwd = item['pwd']
        desc = item['atr']
        if key in tmp_dict:
            tmp_acct = dict()
            tmp_acct['eml'] = email
            tmp_acct['pwd'] = pwd
            tmp_dict[key]['accts'].append(tmp_acct)
        else:
            tmp_dict[key] = dict()
            tmp_dict[key]['accts'] = list()
            tmp_dict[key]['desc'] = desc
            tmp_dict[key]['name'] = src
            tmp_acct = dict()
            tmp_acct['eml'] = email
            tmp_acct['pwd'] = pwd
            tmp_dict[key]['accts'].append(tmp_acct)
    breach_info = tmp_dict


    return json.dumps(breach_info)
