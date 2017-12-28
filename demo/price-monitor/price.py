import traceback
import json
import sys
import time
from importlib import import_module
from PeriodicPusher import PeriodicPusher, Message
from PeriodicPusher.Utils import Log, HttpHelper
from plugin.exchange import *

if __name__ != '__main__':
    exit()

if len(sys.argv[1]) < 2:
    Log.log('Missing config file.', True)
    exit()

pp = PeriodicPusher(sys.argv[1])
price_dict = dict()
cny_exchange_rate = [0, 0]

def get_cny_exchange_rate():
    now = time.time()
    # Update CNY exchange rate per hour.
    if now - cny_exchange_rate[1] < 3600:
        return cny_exchange_rate[0]
    Log.log('Update CNY exchange rate...')
    rate = get_exchange_rate()
    if rate >= 0:
        cny_exchange_rate[0] = rate
        cny_exchange_rate[1] = now
    Log.log('USD:CNY = {}'.format(cny_exchange_rate[0]))
    return cny_exchange_rate[0]


def need_report(p1, p2, delta):
    high = p2 * (100 + delta) /100
    low = p2 * (100 - delta) /100
    if p1 > high or p1 < low:
        return True
    else:
        return False

@pp.prepare
def init_price_dict(config):
    global price_dict
    Log.log('Price init...')
    msg = ''
    # Go through all handles
    for handle in config['HANDLE']:
        handle_impl = import_module('plugin.{}'.format(handle['HANDLE_NAME']))
        for currency_pair in handle['CURRENCY']:
            c1 = currency_pair['source_currency']
            c2 = currency_pair['target_currency']
            get_price = handle_impl.get_price_generator(c1, c2)
            price = get_price()
            desc = '{} {}:{}'.format(handle['HANDLE_NAME'], c1, c2)
            msg += '{} {}; '.format(desc, price)
            price_dict.update({ desc : { 'get_price' : get_price, 'last_report' : price } })
    Log.log(msg)
    Log.log('Price init finished.')



@pp.notification_register
def check_price(config):
    msg = ''
    log_msg = ''
    global price_dict
    Log.log('Check price...')
    for desc in price_dict:
        currency_handle = price_dict[desc]
        price = currency_handle['get_price']()
        if price >= 0:
            log_msg += '{} {}; '.format(desc, price)
            if need_report(price, currency_handle['last_report'], config['THRESHOLD']):
                msg += '\n\n{} current {}, last report {}\n\n'.format(desc, price, currency_handle['last_report'])
                currency_handle['last_report'] = price
                price_dict.update({ desc : currency_handle })
    Log.log(log_msg)
    if msg == '':
        return None
    return Message(msg)

if __name__ == '__main__':
    pp.run()

