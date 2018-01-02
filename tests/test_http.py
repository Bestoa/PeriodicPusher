import http.server
import socketserver
import threading
from PeriodicPusher.Utils import HttpHelper

httpd = socketserver.TCPServer(('', 8008), http.server.SimpleHTTPRequestHandler)
server = threading.Thread(target=httpd.serve_forever)

class TestHttp:
    @classmethod
    def setup_class(cls):
        server.daemon = True
        print('Start http server...')
        server.start()

    @classmethod
    def teardown_class(cls):
        print('Stop http server...')
        httpd.shutdown()

    def test_http_200(self):
        r = HttpHelper.get('http://127.0.0.1:8008/tests/index.html')
        assert r.text == 'Hello\n'

    def test_http_404(self):
        r = HttpHelper.get('http://127.0.0.1:8008/invalid')
        assert r == None

    def test_http_err_check(self):
        r = HttpHelper.get('http://127.0.0.1:8008/tests/index.html', err_check=lambda x:True)
        assert r == None
        r = HttpHelper.get('http://127.0.0.1:8008/tests/index.html', err_check=lambda x:False)
        assert r.text == 'Hello\n'

