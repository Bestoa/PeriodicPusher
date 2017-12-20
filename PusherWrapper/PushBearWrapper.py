import requests
import json
from urllib.parse import urlencode
import sys
sys.path.append('../')
import Log
import traceback

class Pusher:
    def __init__(self, config):
        self.config = config

    def push(self, msg):
        try:
            content = { 'text' : self.config['TITLE'], 'desp' : str(msg) }
            url = '{}{}&{}'.format(self.config['API_BASE'], self.config['KEY'], urlencode(content))
            r = requests.get(url)
            if r.status_code != 200:
                Log.log('Request failed, status code: {}'.format(r.status_code), True)
            res = json.loads(r.text)
            if res['code'] != 0:
                Log.log('Request failed, message: {}'.format(res.message), True)
        except Exception:
            Log.log(traceback.format_exc(), True)
