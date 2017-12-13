class Pusher:
    def __init__(self, config):
        print('Pusher data: %s' % str(config))

    def push(self, msg):
        print('Get push message: %s' % str(msg))

