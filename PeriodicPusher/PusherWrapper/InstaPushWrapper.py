from instapush import Instapush, App
import traceback
from PeriodicPusher.Utils import Log

class Pusher:
    def __init__(self, config):
        self.config = config
        self.app = App(appid = self.config['APPID'], secret = self.config['SECRET'])

    def push(self, msg):
        try:
            ret = self.app.notify(event_name = self.config['EVENT_NAME'], trackers = { self.config['TRACKERS']: str(msg) })
        except Exception:
            Log.log_error(traceback.format_exc())
            return False
        if ret == None:
            Log.log_error('Unknown error.')
            return False
        if ret['error']:
            Log.log_error('Push error, msg: {}'.format(ret['msg']))
            return False
        return True

