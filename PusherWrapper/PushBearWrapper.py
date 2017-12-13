import requests
import json
from urllib.parse import urlencode
class Pusher:
    def __init__(self, config):
        self.config = config

    def push(self, msg):
        try:
            content = { 'text' : self.config['TITLE'], 'desp' : str(msg) }
            url = '%s%s&%s' % (self.config['API_BASE'], self.config['KEY'], urlencode(content))
            print(url)
            r = requests.get(url)
            if r.status_code != 200:
                print('Request failed, status code: %d' % r.status_code)
            res = json.loads(r.text)
            if res['code'] != 0:
                print('Request failed, message: %s' % res.message)
        except:
            print('Exception happened.')
