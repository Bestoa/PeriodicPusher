import time

def log(msg, level = 'DEBUG'):
    cur_time = time.ctime()
    if level == 'ERROR':
        # Error: red 
        format_time = '\033[1;31m' + cur_time + '\033[0m'
    elif level == 'WARNING':
        # Warning: yellow
        format_time = '\033[1;33m' + cur_time + '\033[0m'
    else:
        # Debug: green
        format_time = '\033[1;32m' + cur_time + '\033[0m'
    print('{} {}'.format(format_time, msg))

def log_error(msg):
    log(msg, 'ERROR')

def log_warning(msg):
    log(msg, 'WARNING')

def log_debug(msg):
    log(msg, 'DEBUG')

