# For test only
import json
from PeriodicPusher.PusherWrapper import TestCallback
from PeriodicPusher.Utils import Log
class Pusher:
    def __init__(self, config):
        Log.log_debug('Pusher data: {}'.format(json.dumps(config, indent = 4)))

    def push(self, msg):
        Log.log_debug('Get push message: {}'.format(msg))
        TestCallback.callback.put(msg)
        return True

