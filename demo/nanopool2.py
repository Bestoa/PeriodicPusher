import requests
import json
import sys
import time
sys.path.append('../')
from PeriodicPusher import PeriodicPusher

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    print('Missing config files.')
    exit()

pp = PeriodicPusher(sys.argv[1])
is_offline = False

@pp.register
def offline_checker(config):
    global is_offline
    print('Offline check...')
    try:
        r = requests.get(config['API_BASE'] + config['ACCOUNT'])
        if r.status_code != 200:
            print('Request failed, status: ' + r.status_code)
            return (None, False);
        result = json.loads(r.text)
        if not result['status']:
            print('Api call failed, error:  ' + result['error'])
            return (None, False);
        if result['data'] < config['THRESHOLD']:
            if not is_offline:
                is_offline = True
                return (result['data'], True);
            else:
                print('Offline, but message has already been pushed. Skip...')
                return (None, False);
        else:
            if is_offline:
                is_offline = False
            print('Online!')
            return (None, False);
    except:
        print('Exception happened.')
        return (None, False);

if __name__ == '__main__':
    pp.run()

