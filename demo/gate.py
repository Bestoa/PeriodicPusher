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
            return 0
        result = json.loads(r.text)
        if result['result'] != "true":
            return 0
        return result['last']
    except:
        return 0

@pp.init_sub
def init_price_list(config):
    i = 0
    global price_list
    while i < len(config['CURRENCY']):
        api = config['API_BASE'] + list(config['CURRENCY'][i].keys())[0]
        price = get_price(api)
        price_list.append([api, list(config['CURRENCY'][i].values())[0], price, price])
        i += 1
    print(price_list)



@pp.register
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
                msg += str(price_list[i][1]) + ' ' + str(price) + ' '
                price_list[i][3] = price
        i += 1
    print(price_list)
    if not msg:
        msg = None
    return (msg, False)

if __name__ == '__main__':
    pp.run()
