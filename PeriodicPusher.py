import json
import time
import os
import sched
import PusherWrapper
from importlib import import_module

class PeriodicPusher:
    def log(self, msg):
        cur_time = time.asctime(time.localtime(time.time()))
        format_time = '\033[1;32;40m' + cur_time + '\033[0m'
        print(format_time + ' ' + msg)

    def check_mute(self):
        if not self.config_mute['NEED_MUTE']:
            return False
        hour = time.localtime(time.time()).tm_hour
        mute_start = self.config_mute['MUTE_START']
        mute_end = self.config_mute['MUTE_END']
        if mute_start > mute_end:
            if hour >= mute_start or hour < mute_end:
                return True
        elif hour >= mute_start and hour < mute_end:
            return True 
        return False

    def push_to_user(self, msg, importart = False):
        self.log('Push message:' + str(msg))
        if not importart and self.check_mute():
            self.log('Mute Message')
            return
        self.pusher.push(msg)

    def notify_once(self):
        msg, important = self.do_notify(self.config_priv)
        if msg:
            self.push_to_user(msg, important)

    def notify_loop(self, interval):
        self.schedule.enter(interval, 0, self.notify_loop, kwargs = { 'interval': interval })
        self.notify_once()

    def run(self):
        if not self.do_notify:
            self.log('Must set do_notify method before call run!')
            return
        self.log('Start')
        self.schedule.enter(0, 0, self.notify_loop, kwargs = { 'interval': self.config['INTERVAL'] })
        self.schedule.run()

    def register(self, func):
        self.do_notify = func

    def init_sub(self, func):
        func(self.config_priv)

    def __init__(self, config_file):
        config_json = open(config_file).read()
        self.config = json.loads(config_json)
        self.log('Config: ' + str(self.config))

        pusher_wrapper = import_module('PusherWrapper.' + self.config['PUSHER_NAME'])
        
        self.config_mute = self.config['mute_data']
        self.config_priv = self.config['private_data']
        
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.pusher = pusher_wrapper.Pusher(self.config['pusher_data'])
        self.do_notify = None

