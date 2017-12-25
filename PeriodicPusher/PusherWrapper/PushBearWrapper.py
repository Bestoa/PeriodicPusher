from urllib.parse import urlencode
import traceback
import json
from PeriodicPusher.Utils import Log, HttpHelper

class Pusher:
    def __init__(self, config):
        self.config = config

    def err_check(self, text):
        res = json.loads(text)
        if res['code'] != 0:
            Log.log('Request failed, message: {}'.format(res['message']), True)
            return True
        return False

    def push(self, msg):
        content = { 'text' : self.config['TITLE'], 'desp' : str(msg) }
        url = '{}{}&{}'.format(self.config['API_BASE'], self.config['KEY'], urlencode(content))
        HttpHelper.get(url, err_check = self.err_check)

