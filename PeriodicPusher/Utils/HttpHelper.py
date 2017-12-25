import requests
import traceback
from . import Log

# Get target with retry
def get(url, retry = 3, err_check = None):
    while retry > 0:
        try:
            with requests.get(url) as r:
                if r.status_code != 200:
                    Log.log('Request failed, status code: {}'.format(r.status_code), True)
                    retry -= 1
                    Log.log('Retry = {}'.format(retry), True)
                    continue
                if err_check and err_check(r.text):
                    retry -= 1
                    Log.log('Retry = {}'.format(retry), True)
                    continue
                return r.text 
        # Do not catch ctrl-c
        except Exception:
            Log.log(traceback.format_exc(), True)
            retry -= 1
            Log.log('Retry = {}'.format(retry), True)
    return None

