import requests
import traceback
from . import Log

# Get target with retry
def get(url, retry = 3, err_check = None, params = None):
    while retry > 0:
        try:
            with requests.get(url, params) as r:
                if r.status_code != 200:
                    Log.log_error('Request failed, status code: {}'.format(r.status_code))
                    retry -= 1
                    Log.log_warning('Retry = {}'.format(retry))
                    continue
                if err_check and err_check(r):
                    retry -= 1
                    Log.log_warning('Retry = {}'.format(retry))
                    continue
                return r
        # Do not catch ctrl-c
        except Exception:
            Log.log_error(traceback.format_exc())
            retry -= 1
            Log.log_warning('Retry = {}'.format(retry))
    return None

