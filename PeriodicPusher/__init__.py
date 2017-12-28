import json
import time
import os
import sched
from importlib import import_module
from .Utils import Log

__VERSION__ = '0.0.2'
__AUTHOR__ = 'Besto'
__NAME__ = 'PeriodicPusher'

class Message:
    def __init__(self, msg, important = False):
        self.msg = msg
        self.important = important

class PeriodicPusher:
    def check_mute(self):
        if not self.config_mute['NEED_MUTE']:
            return False
        hour = time.localtime(time.time()).tm_hour
        mute_start = self.config_mute['MUTE_START']
        mute_end = self.config_mute['MUTE_END']
        # Case 1: mute on night such as 22 - 6
        if mute_start > mute_end:
            if hour >= mute_start or hour < mute_end:
                return True
        # Case 2: mute on day such as 11 - 13
        elif hour >= mute_start and hour < mute_end:
            return True 
        return False

    def push_to_user(self, msg):
        Log.log('Push message: {}'.format(msg.msg))
        # Never mute important messages
        if not msg.important and self.check_mute():
            Log.log('Mute Message')
            return
        # Call pusher
        self.pusher.push(msg.msg)

    def notify_once(self):
        # Get message from implementation
        msg = self.get_notification(self.config_priv)
        # Don't push empty message
        if msg:
            self.push_to_user(msg)

    def notify_loop(self, interval, loop):
        # Next notification
        if not loop:
            return
        if loop > 0:
            loop -= 1
        self.schedule.enter(interval, 0, self.notify_loop, kwargs = { 'interval': interval, 'loop': loop })
        self.notify_once()

    def run(self, loop = -1):
        if not self.get_notification:
            Log.log('Must set get_notification method before call run!', True)
            return
        Log.log('Start')
        self.schedule.enter(0, 0, self.notify_loop, kwargs = { 'interval': self.config['INTERVAL'], 'loop': loop })
        self.schedule.run()

    def notification_register(self, func):
        # Register notification, this is mandatory and will be invoked periodicly
        self.get_notification = func

    def prepare(self, func):
        # Register prepare, this is optional and just be called once
        func(self.config_priv)

    def __init__(self, config_file):
        config_json = open(config_file).read()
        self.config = json.loads(config_json)
        Log.log('Config: {}'.format(self.config))

        pusher_wrapper = import_module('PeriodicPusher.PusherWrapper.%s' % self.config['PUSHER_NAME'])
        
        self.config_mute = self.config['mute_data']
        self.config_priv = self.config['private_data']
        
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.pusher = pusher_wrapper.Pusher(self.config['pusher_data'])
        self.get_notification = None

