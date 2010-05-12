
import time

class DefaultTimer(object):
    """ The default timer uses the time provider by the operating system """

    def time(self):
        return time.time()


