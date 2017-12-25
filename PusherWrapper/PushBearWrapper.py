from urllib.parse import urlencode
import traceback
import json
import sys
sys.path.append('../')
import Log
import HttpHeler

class Pusher:
    def __init__(self, config):
        self.config = config

    def err_check(text):
        res = json.loads(text)
        if res['code'] != 0:
            Log.log('Request failed, message: {}'.format(res['message']), True)
            return True
        return False

    def push(self, msg):
        content = { 'text' : self.config['TITLE'], 'desp' : str(msg) }
        url = '{}{}&{}'.format(self.config['API_BASE'], self.config['KEY'], urlencode(content))
        HttpHeler.get(url, err_check = self.err_check)

