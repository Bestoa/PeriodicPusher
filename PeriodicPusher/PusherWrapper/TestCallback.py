import threading

class Callback:
    def __init__(self):
        self.mutex = threading.Lock()
        self.msg_queue = list()

    def put(self, msg):
        self.mutex.acquire()
        self.msg_queue.append(msg)
        self.mutex.release()

    def get(self):
        ret = None
        self.mutex.acquire()
        if len(self.msg_queue) > 0:
            ret = self.msg_queue.pop()
        self.mutex.release()
        return ret 

callback = Callback()
