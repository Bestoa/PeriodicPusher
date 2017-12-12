import requests
import json
import sys
import time
sys.path.append('../')
from PeriodicPusher import PeriodicPusher

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    print('Missing config file.')
    exit()

pp = PeriodicPusher(sys.argv[1])

def build_msg(origin_msg):
    msg = list()
    msg.append({'hashrate' : origin_msg['hashrate']})
    msg.append({'balance' : origin_msg['balance']})
    msg.append({'avgHashrate' : sorted(origin_msg['avgHashrate'].items(), key = lambda x:int(x[0][1:]))})
    return msg

@pp.register
def hourly_notify(config):
    try:
        r = requests.get(config['API_BASE'] + config['ACCOUNT'])
        if r.status_code != 200:
            print('Request failed, status = ' + r.status_code)
            return (None, False);
        result = json.loads(r.text)
        if not result['status']:
            print('Api call failed, error =  ' + result['error'])
            return (None, False);
        else:
            return (build_msg(result['data']), False)
    except Exception as e:
        print('Request exception: ' + e)
        return (None, False);

if __name__ == '__main__':
    pp.run()

