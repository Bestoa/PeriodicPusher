import sys
sys.path.append('../')
from PeriodicPusher import PeriodicPusher

if __name__ != '__main__':
    exit()

if len(sys.argv) < 2:
    exit()

pp = PeriodicPusher(sys.argv[1])

def demo_init(config):
    print('From init, config: %s' % str(config))

def demo_do_notify(config):
    print('From do_notify, config: %s' % str(config))
    return ('Test', False)

pp.init_sub(demo_init)
pp.register(demo_do_notify)
pp.run()
