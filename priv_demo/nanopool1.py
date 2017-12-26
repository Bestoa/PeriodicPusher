import traceback
import json
import sys
import time
from PeriodicPusher import PeriodicPusher, Message
from PeriodicPusher.Utils import Log, HttpHelper

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

def err_check(text):
    result = json.loads(text)
    if not result['status']:
        Log.log('Api call failed, error: {}'.format(result['error']), True)
        return True
    return False

@pp.notification_register
def hourly_notify(config):
    url = config['API_BASE'] + config['ACCOUNT']
    text = HttpHelper.get(url, err_check = err_check)
    if text:
        res = json.loads(text)
        return Message(build_msg(res['data']))

if __name__ == '__main__':
    pp.run()

