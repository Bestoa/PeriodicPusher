from urllib.parse import urlencode
import traceback
from PeriodicPusher.Utils import Log, HttpHelper

class Pusher:
    def __init__(self, config):
        self.config = config

    def err_check(self, r):
        res = r.json()
        if res['code'] != 0:
            Log.log('Request failed, message: {}'.format(res['message']), True)
            return True
        return False

    def push(self, msg):
        params = { 'sendkey' : self.config['KEY'], 'text' : self.config['TITLE'], 'desp' : str(msg) }
        r = HttpHelper.get(self.config['API_BASE'], err_check = self.err_check, params = params)
        if r == None:
            return False
        return True

