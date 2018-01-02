from PeriodicPusher.Utils import Log, HttpHelper

API = 'https://min-api.cryptocompare.com/data/price'

def err_check(r):
    result = r.json()
    if 'Response' in result:
        Log.log_error('Request failed, error message: {}'.format(result['Message']))
        return True
    return False

def get_price_generator(c1, c2):
    params = { 'fsym' : c1, 'tsyms' : c2 }
    def get_price():
        r = HttpHelper.get(API, err_check = err_check, params = params)
        if r:
            result = r.json()
            return result[c2]
        else:
            return -1
    return get_price

