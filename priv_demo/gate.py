import requests
import json
import sys
sys.path.append('../')
from PeriodicPusher import PeriodicPusher, Message

if __name__ != '__main__':
    exit()

if len(sys.argv[1]) < 2:
    print('Missing config file.')

pp = PeriodicPusher(sys.argv[1])
price_dict = dict()

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

@pp.prepare
def init_price_dict(config):
    global price_dict
    print('Price init...')
    msg = ''
    for currency_pair in config['CURRENCY']:
        desc = currency_pair['desc']
        api = config['API_BASE'] + currency_pair['api']
        price = get_price(api)
        msg += '{} {} '.format(desc, price)
        price_dict.update({ desc : { 'api' : api, 'last_report' : price } })
    print(msg)
    print('Price init finished.')



@pp.notification_register
def check_price(config):
    msg = ''
    log_msg = ''
    global price_dict
    print('Check price...')
    for currency in price_dict:
        price = get_price(price_dict[currency]['api'])
        if price != 0:
            log_msg += '{} {} '.format(currency, price)
            if need_report(price, price_dict[currency]['last_report'], config['THRESHOLD']):
                msg += '\n\n{} current {}, last report {}\n\n'.format(currency, price, price_dict[currency]['last_report'])
                price_dict[currency]['last_report'] = price
    print(log_msg)
    if msg == '':
        return None
    return Message(msg)

if __name__ == '__main__':
    pp.run()
