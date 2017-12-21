import requests
import sys
import json
sys.path.append('../')
import Log
import traceback

def get_exchange_rate(base = 'usd', target = 'CNY'):
    try:
        r = requests.get('https://api.fixer.io/latest?base={}'.format(base))
        if r.status_code != 200:
            Log.log('Request failed, status code: {}'.format(r.status_code), True)
            return -1 
        res = json.loads(r.text)
        if 'error' in res:
            Log.log(res['error'], True)
            return -1
        if target not in res['rates']:
            Log.log('No such target currency: {}'.format(target), -1)
            return -1 
        return res['rates'][target]
    except:
        Log.log(traceback.format_exc(), True)
        return -1

