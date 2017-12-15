import sys
sys.path.append('../')
from PeriodicPusher import PeriodicPusher

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
    # The first return value is the message you want to push to user, the second
    # shows whether this message is important or not.
    return ('Test', False)

# Register init and get_notification
pp.prepare(demo_init)
pp.notification_register(demo_get_notification)
# Call run to start
pp.run()
