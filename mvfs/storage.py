
import os
import time

from mvfs.exceptions import MVFSException
from mvfs.utils import mkdir_p

class DefaultTimer(object):
    """ The default timer uses the time provider by the operating system """

    def time(self):
        return int(time.time())


class Storage(object):

    class NotFound(MVFSException):
        def __init__(self, path):
            super(Storage.NotFound, self).__init__('Base path not found: %s' % path)

    class InvalidPath(MVFSException):
        def __init__(self, path):
            super(Storage.InvalidPath, self).__init__('Invalid base path: '\
                '%s. Expecting a folder.' % path)

    class AlreadyExists(MVFSException): pass

    timer = DefaultTimer()

    def __init__(self, base_path):
        if not os.path.exists(base_path):
            raise Storage.NotFound, base_path

        if not os.path.isdir(base_path):
            raise Storage.InvalidPath, base_path

        self.base_path = base_path

    def exists(self, vpath, ts=None):
        """ Check path existence in virtual file system """
        path = self._real_path(vpath, ts)
        return path is not None and os.path.exists(path)

    def open(self, vpath, mode='r', ts=None):
        if mode in ('w', 'w+') and ts is None:
            ts = self.timer.time()

        return open(self._real_path(vpath, ts=ts), mode)

    def get_versions(self, vpath):
        path = os.path.join(self.base_path, vpath)
        return sorted([int(f) for f in os.listdir(path)], reverse=True)

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
        return max([int(f) for f in os.listdir(dir)])
            

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

