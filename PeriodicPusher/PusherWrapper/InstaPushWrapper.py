from instapush import Instapush, App

class Pusher:
    def __init__(self, config):
        self.config = config
        self.app = App(appid = self.config['APPID'], secret = self.config['SECRET'])

    def push(self, msg):
        self.app.notify(event_name = self.config['EVENT_NAME'], trackers = { self.config['TRACKERS']: str(msg) })

