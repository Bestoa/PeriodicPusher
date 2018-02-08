from pushover import init, Client
import traceback
from PeriodicPusher.Utils import Log

class Pusher:
    def __init__(self, config):
        self.config = config
        init(self.config['API_TOKEN'])

    def push(self, msg):
        try:
            Client(self.config['KEY']).send_message(msg, title = self.config['TITLE'])
        except Exception:
            Log.log_error(traceback.format_exc())
            return False
        return True
