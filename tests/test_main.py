from PeriodicPusher import PeriodicPusher, Message
from PeriodicPusher.Utils import Log
from PeriodicPusher.PusherWrapper import TestCallback

def gen_notification(config, msg = 'TEST MESSAGE'):
    assert 'PRIVATE_DATA' in config
    assert config['PRIVATE_DATA'] == 'test-private-data'
    return Message(msg)

def gen_multi_notification(config):
    return [gen_notification(config, 'TEST1'), gen_notification(config, 'TEST2'), gen_notification(config, 'TEST3')]

def test_once():
    config = {
            'INTERVAL' : 1,
            'PUSHER_NAME' : 'FakeWrapper',
            'pusher_data' : { 'PUSHER_DATA' : 'test-pusher-data' },
            'mute_data' : { 'NEED_MUTE' : False },
            'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
            }
    pp = PeriodicPusher(config  = config)
    pp.notification_register(gen_notification)
    pp.run(1)
    assert TestCallback.callback.get() == 'TEST MESSAGE'

def test_none_message_once():
    config = {
            'INTERVAL' : 1,
            'PUSHER_NAME' : 'FakeWrapper',
            'pusher_data' : { 'PUSHER_DATA' : 'test-pusher-data' },
            'mute_data' : { 'NEED_MUTE' : False },
            'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
            }
    pp = PeriodicPusher(config  = config)
    pp.notification_register(lambda x: None)
    pp.run(1)
    assert TestCallback.callback.get() == None

def test_loop():
    config = {
            'INTERVAL' : 1,
            'PUSHER_NAME' : 'FakeWrapper',
            'pusher_data' : { 'PUSHER_DATA' : 'test-pusher-data' },
            'mute_data' : { 'NEED_MUTE' : False },
            'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
            }
    pp = PeriodicPusher(config  = config)
    pp.notification_register(gen_notification)
    pp.run(3)
    assert TestCallback.callback.get() == 'TEST MESSAGE'
    assert TestCallback.callback.get() == 'TEST MESSAGE'
    assert TestCallback.callback.get() == 'TEST MESSAGE'
    assert TestCallback.callback.get() == None

def test_mute():
    config = {
            'INTERVAL' : 1,
            'PUSHER_NAME' : 'FakeWrapper',
            'pusher_data' : { 'PUSHER_DATA' : 'test-pusher-data' },
            'mute_data' : { 'NEED_MUTE' : True, 'MUTE_START' : 0, 'MUTE_END' : 24 },
            'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
            }
    pp = PeriodicPusher(config  = config)
    pp.notification_register(lambda x:Message('TEST'))
    pp.run(1)
    assert TestCallback.callback.get() == None
    pp.notification_register(lambda x:Message('TEST', True))
    pp.run(1)
    assert TestCallback.callback.get() == 'TEST'

def test_push_retry():
    config = {
            'INTERVAL' : 1,
            'PUSHER_NAME' : 'PushOverWrapper',
            'pusher_data' : { 'API_TOKEN': '', 'KEY' : '', 'TITLE' : '' },
            'mute_data' : { 'NEED_MUTE' : False },
            'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
            }
    pp = PeriodicPusher(config  = config)
    pp.notification_register(gen_notification)
    pp.run(1)
    assert pp.push_retry_counts == 3
    assert pp.push_fail_counts == 1

def test_multi_msg():
    config = {
            'INTERVAL' : 1,
            'PUSHER_NAME' : 'FakeWrapper',
            'pusher_data' : { 'PUSHER_DATA' : 'test-pusher-data' },
            'mute_data' : { 'NEED_MUTE' : False },
            'private_data': { 'PRIVATE_DATA' : 'test-private-data' }
            }
    pp = PeriodicPusher(config  = config)
    pp.notification_register(gen_multi_notification)
    pp.run(1)
    assert TestCallback.callback.get() == 'TEST3'
    assert TestCallback.callback.get() == 'TEST2'
    assert TestCallback.callback.get() == 'TEST1'
    assert TestCallback.callback.get() == None
