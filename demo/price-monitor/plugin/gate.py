from PeriodicPusher.Utils import Log, HttpHelper

API = 'http://data.gate.io/api2/1/ticker/'

def err_check(r):
    result = r.json()
    if result['result'] != "true":
        Log.log('Request failed, error message: {}'.format(result['message']), True)
        return True
    return False

def get_price_generator(c1, c2):
    url = '{}{}_{}'.format(API, c1, c2)
    def get_price():
        r = HttpHelper.get(url, err_check = err_check)
        if r:
            result = r.json()
            return result['last']
        else:
            return -1
    return get_price

