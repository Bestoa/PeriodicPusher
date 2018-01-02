import traceback
import sys
import json
from PeriodicPusher.Utils import Log, HttpHelper

def err_check(r):
    res = r.json()
    if 'error' in res:
        Log.log_error(res['error'])
        return True
    return False

def get_exchange_rate(base = 'usd', target = 'CNY'):
    api = 'https://api.fixer.io/latest'
    params = { 'base' : base }
    r = HttpHelper.get(api, err_check = err_check, params = params)
    if r == None:
        return -1
    res = r.json()
    if target not in res['rates']:
        Log.log_error('No such target currency: {}'.format(target))
        return -1
    return res['rates'][target]

