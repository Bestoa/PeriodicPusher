import requests
import Log
import traceback

# Get target with retry
def get(url, retry = 3, err_check = None):
    while retry > 0:
        try:
            with requests.get(url) as r:
                if r.status_code != 200:
                    Log.log('Request failed, status code: {}'.format(r.status_code), True)
                    Log.log('Retry...', True)
                    retry -= 1
                    continue
                if err_check and err_check(r.text):
                    Log.log('Retry...', True)
                    retry -= 1
                    continue
                return r.text 
        except:
            Log.log(traceback.format_exc(), True)
            Log.log('Retry...', True)
            retry -= 1
    return None

