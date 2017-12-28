from instapush import Instapush, App
from PeriodicPusher.Utils import Log

class Pusher:
    def __init__(self, config):
        self.config = config
        self.app = App(appid = self.config['APPID'], secret = self.config['SECRET'])

    def push(self, msg):
        ret = self.app.notify(event_name = self.config['EVENT_NAME'], trackers = { self.config['TRACKERS']: str(msg) })
        if ret == None:
            Log.log('Unknown error.', True)
            return False
        if ret['error']:
            Log.log('Push error, msg: {}'.format(ret['msg']), True)
            return False
        return True

