import json
import os
import requests

def lambda_handler(event, context):
    txt_key = '{"BS_API_KEY":"6f77cd0dfb00fb7860687eef1ec964ec"}'
    json_key = json.loads(txt_key)
    API_KEY = json_key['BS_API_KEY']
    API_URL = 'https://api.breachsense.com/creds'
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

lambda_handler({"search_string":"mgargiullo@gmail.com"}, "")