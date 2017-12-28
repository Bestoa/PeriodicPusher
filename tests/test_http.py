import sys
from PeriodicPusher.Utils import HttpHelper

def test_http_200():
    r = HttpHelper.get('http://127.0.0.1:8000')
    assert r.text == 'Hello\n'

def test_http_404():
    r = HttpHelper.get('http://127.0.0.1:8000/invalid')
    assert r == None 

def test_http_err_check():
    r = HttpHelper.get('http://127.0.0.1:8000', err_check=lambda x:True)
    assert r == None 
    r = HttpHelper.get('http://127.0.0.1:8000', err_check=lambda x:False)
    assert r.text == 'Hello\n'
