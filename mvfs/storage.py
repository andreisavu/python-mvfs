
import os
import time

from mvfs.exceptions import MVFSException
from mvfs.utils import mkdir_p

class DefaultTimer(object):
    """ The default timer uses the time provider by the operating system """

    def time(self):
        return time.time()


class Storage(object):

    class NotFound(MVFSException):
        def __init__(self, path):
            super(Storage.NotFound, self).__init__('Base path not found: %s' % path)

    class InvalidPath(MVFSException): pass

    class AlreadyExists(MVFSException): pass

    timer = DefaultTimer()

    def _get_time(self):
        return "%.5f" % self.timer.time()

    def __init__(self, base_path):
        if base_path[0] != '/':
            raise Storage.InvalidPath, "The base path should be absolute."

        if not os.path.exists(base_path):
            raise Storage.NotFound, base_path

        if not os.path.isdir(base_path):
            raise Storage.InvalidPath, "Expecting a folder: %s" % base_path

        self.base_path = base_path

    def exists(self, vpath, ts=None):
        """ Check path existence in virtual file system """
        path = self._real_path(vpath, ts)
        return path is not None and os.path.exists(path)

    def open(self, vpath, mode='r', ts=None):
        if mode in ('w', 'w+') and ts is None:
            ts = self._get_time()
            while self.exists(vpath, ts): 
                ts = "%.5f" % (float(ts) + 0.00001)    # move the new version a bit into the future

        return open(self._real_path(vpath, ts=ts), mode)

    def get_versions(self, vpath):
        path = os.path.join(self.base_path, vpath)
        return ["%.5f" % el for el in \
            sorted((float(f) for f in os.listdir(path)), reverse=True)]

    def _real_path(self, vpath, ts=None):
        """ Build a real file path from a virtual path 

        If ts is None return the path of the latest version.
        """
        dir = os.path.join(self.base_path, vpath)

        if not os.path.exists(dir):
            if ts is None: 
                return None

            head, tail = os.path.split(dir)
            while head != self.base_path:
                if self._contains_files(head):
                    raise Storage.AlreadyExists, "A file with the same name alrady exists."
                head, tail = os.path.split(head)
        
            mkdir_p(dir)

        elif os.path.isdir(dir) and self._contains_dirs(dir):
            raise Storage.AlreadyExists, "A directory with the same name already exists."

        if ts is None:
            ts = self._latest_version_ts(dir)

        return os.path.join(dir, str(ts))

    def _latest_version_ts(self, dir):
        return "%.5f" % max([float(f) for f in os.listdir(dir)])
            
    def _contains_dirs(self, dir):
        for f in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, f)): 
                return True
        return False

    def _contains_files(self, dir):
        if not os.path.exists(dir):
            return False
        for f in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, f)):
                return True
        return False

