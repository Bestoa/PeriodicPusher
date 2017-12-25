import traceback
import sys
import json
sys.path.append('../')
import Log
import HttpHelper

def err_check(text):
    res = json.loads(text)
    if 'error' in res:
        Log.log(res['error'], True)
        return True
    return False

def get_exchange_rate(base = 'usd', target = 'CNY'):
    api = 'https://api.fixer.io/latest?base={}'.format(base)
    text = HttpHelper.get(api, err_check = err_check)
    if text == None:
        return -1
    res = json.loads(text)
    if target not in res['rates']:
        Log.log('No such target currency: {}'.format(target), -1)
        return -1
    return res['rates'][target]

