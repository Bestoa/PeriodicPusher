from pushover import init, Client
from PeriodicPusher.Utils import Log

class Pusher:
    def __init__(self, config):
        self.config = config
        init(self.config['API_TOKEN'])

    def push(self, msg):
        Client(self.config['KEY']).send_message(msg, title = self.config['TITLE'])
        return True
