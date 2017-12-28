#Please replace the private config with yours and check the results manually.
from PeriodicPusher.PusherWrapper import InstaPushWrapper
from PeriodicPusher.PusherWrapper import PushBearWrapper
from PeriodicPusher.PusherWrapper import FakeWrapper
from PeriodicPusher.PusherWrapper import TestCallback

def test_instapush_successful():
    config = {
            'APPID' : '5a4207a3a4c48a8ac910716a',
            'SECRET' : '0d123d513168597911d3ebc43a8574c2',
            'EVENT_NAME': 'test-event',
            'TRACKERS' : 'test-message'
            }

    pusher = InstaPushWrapper.Pusher(config)
    assert pusher.push('Hello World') == True

def test_instapush_failed():
    config = {
            'APPID' : '',
            'SECRET' : '',
            'EVENT_NAME': '',
            'TRACKERS' : ''
            }

    pusher = InstaPushWrapper.Pusher(config)
    assert pusher.push('Hello World') == False

def test_pushbear_successful():
    config = {
            'API_BASE': 'https://pushbear.ftqq.com/sub',
            'KEY' : '1730-d255b3761a7f81e53c1c70386513e09e',
            'TITLE' : 'Test'
            }
    pusher = PushBearWrapper.Pusher(config)
    assert pusher.push('Hello World') == True

def test_pushbear_failed():
    config = {
            'API_BASE': 'https://pushbear.ftqq.com/sub',
            'KEY' : '',
            'TITLE' : 'Test'
            }
    pusher = PushBearWrapper.Pusher(config)
    assert pusher.push('Hello World') == False

def test_fakepusher():
    pusher = FakeWrapper.Pusher(None)
    msg = 'THIS IS TEST MESSAGE'
    assert pusher.push(msg) == True
    assert TestCallback.callback.get() == msg
