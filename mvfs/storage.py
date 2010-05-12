
import os
import time
import gzip

from mvfs.exceptions import MVFSException
from mvfs.utils import mkdir_p

class DefaultTimer(object):
    """ The default timer uses the time provider by the operating system """

    def time(self):
        return time.time()

class Opener(object):
    def open(self, path, mode='r'):
        """ When implemented this method should return a file-like object 

        It should be possible to use the returned object as a context manager.
        """
        raise Exception, "Not implemented"

class PlainFileOpener(Opener):
    def open(self, path, mode='r'):
        return open(path, mode)

class GZipFileOpener(Opener):

    class ClosingContextManager(object):
        def __init__(self, thing):
            self.thing = thing

        def __getattr__(self, name):
            return getattr(self.thing, name)

        def __enter__(self):
            return self.thing

        def __exit__(self, *args):
            self.thing.close()


    def open(self, path, mode='r'):
        return self.ClosingContextManager(gzip.open(path, mode))

class Storage(object):

    class NotFound(MVFSException):
        def __init__(self, path):
            super(Storage.NotFound, self).__init__('Base path not found: %s' % path)

    class InvalidPath(MVFSException): pass

    class InvalidFS(MVFSException): pass

    class AlreadyExists(MVFSException): pass

    def _get_time(self):
        return "%.5f" % self.timer.time()

    def __init__(self, base_path, timer=False, opener=False):
        self.timer = timer or DefaultTimer()
        self.opener = opener or GZipFileOpener()

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

        return self.opener.open(self._real_path(vpath, ts=ts), mode)

    def get_versions(self, vpath):
        path = os.path.join(self.base_path, vpath)
        return ["%.5f" % el for el in \
            sorted((float(f) for f in os.listdir(path)), reverse=True)]

    def cleanup(self, versions=None):
        def cleaner(base_path, ids):
            for version in ids[versions:]:
                os.unlink(version)

        self._map_to_vfile(self.base_path, cleaner)

    def _map_to_vfile(self, base_path, fn, *args, **kwargs):
        if self._contains_files(base_path):
            try:
                ids = [os.path.join(base_path, "%.5f" % el) for el in \
                    sorted((float(f) for f in os.listdir(base_path)), reverse=True)]

                fn(base_path, ids, *args, **kwargs)

            except (TypeError, ValueError), e:
                raise InvalidFS, 'Invalid virtual filesystem: %s' % e

        else:
            for el in os.listdir(base_path):
                self._map_to_vfile(os.path.join(base_path, el), fn, *args, **kwargs)

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
                    raise Storage.AlreadyExists, "A file with the same name already exists."
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

