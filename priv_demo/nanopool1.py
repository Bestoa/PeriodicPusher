import requests
import json
import sys
import time
sys.path.append('../')
from PeriodicPusher import PeriodicPusher, Message
import Log
import traceback

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    Log.log('Missing config file.', True)
    exit()

pp = PeriodicPusher(sys.argv[1])

def build_msg(origin_msg):
    msg = list()
    msg.append({'hashrate' : origin_msg['hashrate']})
    msg.append({'balance' : origin_msg['balance']})
    msg.append({'avgHashrate' : sorted(origin_msg['avgHashrate'].items(), key = lambda x:int(x[0][1:]))})
    return str(msg)

@pp.notification_register
def hourly_notify(config):
    try:
        r = requests.get(config['API_BASE'] + config['ACCOUNT'])
        if r.status_code != 200:
            Log.log('Request failed, status: {}'.format(r.status_code), True)
            return None
        result = json.loads(r.text)
        if not result['status']:
            Log.log('Api call failed, error: {}'.format(result['error']), True)
            return None
        else:
            return Message(build_msg(result['data']))
    except Exception:
        Log.log(traceback.foramt_exc(), True)
        return None

if __name__ == '__main__':
    pp.run()

