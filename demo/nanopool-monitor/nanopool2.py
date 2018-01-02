import traceback
import json
import sys
import time
from PeriodicPusher import PeriodicPusher, Message
from PeriodicPusher.Utils import Log, HttpHelper

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    Log.log_error('Missing config files.')
    exit()

pp = PeriodicPusher(sys.argv[1])
last_hashrate = -1

def err_check(r):
    result = r.json()
    if not result['status']:
        Log.log_error('Api call failed, error: {}'.format(result['error']))
        return True
    return False


def get_report_hashrate(config):
    url = config['API_BASE'] + config['ACCOUNT']
    r = HttpHelper.get(url, err_check = err_check)
    if r:
        result = r.json()
        return result['data']
    return -1

@pp.notification_register
def offline_checker(config):
    global last_hashrate
    Log.log_debug('Offline check...')
    current_hashrate = get_report_hashrate(config)
    if current_hashrate >= 0:
        Log.log_debug('Current hashrate is {}'.format(current_hashrate))
        high = last_hashrate * (100 + config['THRESHOLD']) / 100
        low = last_hashrate * (100 - config['THRESHOLD']) / 100
        last_hashrate = current_hashrate
        if current_hashrate > high or current_hashrate < low:
            return Message(current_hashrate, True)
    return None

@pp.prepare
def init(config):
    global last_hashrate
    last_hashrate = get_report_hashrate(config)
    if last_hashrate < 0:
        raise Exception('Init hashrate failed.')
    Log.log_debug('Init hashrate is {}'.format(last_hashrate))

if __name__ == '__main__':
    pp.run()

