from PeriodicPusher.Utils import Log, HttpHelper

API = 'https://x.miguan.in/otc/v7/monitorRecordList'

def err_check(r):
    if r.json()['code'] != 200:
        return True
    return False

def get_price_generator(c1, c2):
    params = { 'orderBy' : 'turnover' }
    def get_price():
        r = HttpHelper.get(API, err_check = err_check, params = params)
        if r:
            return r.json()['result'][0]['cnyPrice']
        else:
            return -1
    return get_price
