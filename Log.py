import time

def log(msg, error = False):
    cur_time = time.asctime(time.localtime(time.time()))
    if error:
        # Error: red 
        format_time = '\033[1;31m' + cur_time + '\033[0m'
    else:
        # Debug: green
        format_time = '\033[1;32m' + cur_time + '\033[0m'
    print('{} {}'.format(format_time, msg))

