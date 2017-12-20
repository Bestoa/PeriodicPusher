import requests
import json
import sys
import time
sys.path.append('../')
from PeriodicPusher import PeriodicPusher, Message

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    print('Missing config files.')
    exit()

pp = PeriodicPusher(sys.argv[1])
last_hashrate = 0

def get_report_hashrate(config):
    try:
        r = requests.get(config['API_BASE'] + config['ACCOUNT'])
        if r.status_code != 200:
            print('Request failed, status: ' + r.status_code)
            return (False, 0)
        result = json.loads(r.text)
        if not result['status']:
            print('Api call failed, error:  ' + result['error'])
            return (False, 0)
        return (True, result['data'])
    except:
        print('Exception happened.')
        return (False, 0)

@pp.notification_register
def offline_checker(config):
    global last_hashrate
    print('Offline check...')
    ret, current_hashrate = get_report_hashrate(config)
    if ret:
        print('Current hashrate is {}'.format(current_hashrate))
        high = last_hashrate * (100 + config['THRESHOLD']) / 100
        low = last_hashrate * (100 - config['THRESHOLD']) / 100
        last_hashrate = current_hashrate
        if current_hashrate > high or current_hashrate < low:
            return Message(current_hashrate, True)
    return None;

@pp.prepare
def init(config):
    global last_hashrate
    ret, last_hashrate = get_report_hashrate(config)
    if not ret:
        raise Exception('Init hashrate failed.')
    print('Init hashrate is %.2f' % last_hashrate)

if __name__ == '__main__':
    pp.run()

