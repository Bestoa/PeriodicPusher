import sys
from PeriodicPusher import PeriodicPusher, Message
from PeriodicPusher.Utils import Log

if __name__ != '__main__':
    exit()

config = {
        'INTERVAL' : 10,
        'PUSHER_NAME' : 'FakeWrapper',
        'pusher_data' : { 'PUSHER_DATA' : 'test-pusher-data' },
        'mute_data' : { 'NEED_MUTE' : False },
        'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
        }

# Create new Pusher
pp = PeriodicPusher(config = config)

def demo_init(config):
    Log.log('From init, config: {}'.format(config))
    # Add your init code here, config contains private_data in json file

def demo_get_notification(config):
    Log.log('From get_notification, config: {}'.format(config))
    # Add your notification here, config contains private_data in json file.
    return Message('Test')

# Register init and get_notification
pp.prepare(demo_init)
pp.notification_register(demo_get_notification)
# Call run to start
pp.run()
