import requests
import time
import csv
import logging
import pandas as pd
from pandas.io.json import json_normalize
try:
    import simplejson as json
except ImportError:
    import json

    
API_KEY = r''
BASE_URL = r'https://www.procyclingstats.com/api/api.php'
CODE = r'ddd-all-riders-api' 
LIMIT = 100
LEVEL = 4
OFFSET = range(0, 4000, 100)

# create an dict of empty lists, keys are column names.
data = {'first_name': [], 'last_name': [],
        'weight': [], 'teamclass': [],
        'sprint': [], 'gc': [],
        'itt': [], 'classic': [],
        'rnk': [], 'pnt': [],
        'birthdate': [], 'nation': [],
        'contract_untill': [], 'team': [],
        'height': [],'id': []}


def api(offset, **kwargs):
    kwargs.update({
            'code': CODE,
            'key': API_KEY,
            'limit': LIMIT,
            'level': LEVEL,
            'offset': offset
        })
    resp = requests.get(BASE_URL, kwargs)
    resp_json = resp.json()
    
    for name in resp_json['riders']:
        data['first_name'].append(name['first_name'])
        data['last_name'].append(name['last_name'])
        data['weight'].append(name['weight'])
        data['teamclass'].append(name['teamclass'])
        data['sprint'].append(name['specialty']['sprint'])
        data['gc'].append(name['specialty']['gc'])
        data['itt'].append(name['specialty']['itt'])
        data['classic'].append(name['specialty']['classic'])
        data['rnk'].append(name['uci_worldranking']['rnk'])
        data['pnt'].append(name['uci_worldranking']['pnt'])
        data['birthdate'].append(name['birthdate'])
        data['nation'].append(name['nation'])
        data['contract_untill'].append(name['contract_untill'])
        data['team'].append(name['team'])
        data['height'].append(name['height'])
        data['id'].append(name['id'])
    
    df = pd.DataFrame(data)
    
    return df


for i in OFFSET:
    try:
        dataframe = api(i)
    except TypeError as te:
        pass

dataframe.to_csv('pcs_2.csv', na_rep = 'None', encoding='utf-8-sig', index = False)