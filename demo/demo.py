import sys
sys.path.append('../')
from PeriodicPusher import PeriodicPusher, Message

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    exit()

# Create new Pusher
pp = PeriodicPusher(sys.argv[1])

def demo_init(config):
    print('From init, config: %s' % str(config))
    # Add your init code here, config contains private_data in json file

def demo_get_notification(config):
    print('From get_notification, config: %s' % str(config))
    # Add your notification here, config contains private_data in json file.
    return Message('Test')

# Register init and get_notification
pp.prepare(demo_init)
pp.notification_register(demo_get_notification)
# Call run to start
pp.run()
