import json, os, requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from _fetch_sec import get_secret
import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    API_KEY = get_secret()
    API_URL = os.environ.get('BS_API_URL')
    PARAMS = {'lic': API_KEY, 's': event['search_string'], 'attr': True,
              'date': str((datetime.today() - relativedelta(months=6)).strftime('%Y%m%d'))}
    req = requests.get(API_URL, params=PARAMS)
    logger.info(req.status_code)
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
