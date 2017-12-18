import requests
import json
import sys
sys.path.append('../')
from PeriodicPusher import PeriodicPusher

if __name__ != '__main__':
    exit()

if len(sys.argv[1]) < 2:
    print('Missing config file.')

pp = PeriodicPusher(sys.argv[1])
# 0 for API
# 1 for description
# 2 for current price
# 3 for last reported price
price_list = list()

def need_report(p1, p2, delta):
    high = p2 * (100 + delta) /100
    low = p2 * (100 - delta) /100
    if p1 > high or p1 < low:
        return True
    else:
        return False

def get_price(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print('Request failed, status code: %d' % r.status_code)
            return 0
        result = json.loads(r.text)
        if result['result'] != "true":
            print('Request failed, error message: %s' % result['message'])
            return 0
        return result['last']
    except:
        print('Get price exception happened.')
        return 0

def get_key(pair):
    return list(pair.keys())[0]

def get_value(pair):
    return list(pair.values())[0]

@pp.prepare
def init_price_list(config):
    i = 0
    global price_list
    while i < len(config['CURRENCY']):
        api = config['API_BASE'] + get_key(config['CURRENCY'][i])
        price = get_price(api)
        price_list.append([api, get_value(config['CURRENCY'][i]), price, 0])
        i += 1
    print('Price init finished.')
    print(price_list)



@pp.notification_register
def check_price(config):
    i = 0
    msg = '' 
    global price_list
    print('Check price')
    while i < len(price_list):
        price = get_price(price_list[i][0])
        if price != 0:
            price_list[i][2] = price
            if need_report(price, price_list[i][3], config['THRESHOLD']):
                msg += '\n\n{} current {}, last report {}\n\n'.format(price_list[i][1], price_list[i][2], price_list[i][3])
                price_list[i][3] = price
        i += 1
    print(price_list)
    if msg == '':
        msg = None
    return (msg, False)

if __name__ == '__main__':
    pp.run()
