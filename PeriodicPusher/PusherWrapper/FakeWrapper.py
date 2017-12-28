import sys
from PeriodicPusher.Utils import Log
class Pusher:
    def __init__(self, config):
        Log.log('Pusher data: {}'.format(config))

    def push(self, msg):
        Log.log('Get push message: {}'.format(msg))
        return True

