import requests
import traceback
from . import Log

# Get target with retry
def get(url, retry = 3, err_check = None, params = None):
    while retry > 0:
        try:
            with requests.get(url, params) as r:
                if r.status_code != 200:
                    Log.log('Request failed, status code: {}'.format(r.status_code), True)
                    retry -= 1
                    Log.log('Retry = {}'.format(retry), True)
                    continue
                if err_check and err_check(r):
                    retry -= 1
                    Log.log('Retry = {}'.format(retry), True)
                    continue
                return r
        # Do not catch ctrl-c
        except Exception:
            Log.log(traceback.format_exc(), True)
            retry -= 1
            Log.log('Retry = {}'.format(retry), True)
    return None

