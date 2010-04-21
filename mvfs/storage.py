
import os

from mvfs.exceptions import MVFSException

class Storage(object):

    class NotFound(MVFSException):
        def __init__(self, path):
            super(Storage.NotFound, self).__init__('Base path not found: %s' % path)

    class InvalidPath(MVFSException):
        def __init__(self, path):
            super(Storage.InvalidPath, self).__init__('Invalid base path: '\
                '%s. Expecting a folder.' % path)

    def __init__(self, base_path):
        if not os.path.exists(base_path):
            raise Storage.NotFound, base_path

        if not os.path.isdir(base_path):
            raise Storage.InvalidPath, base_path

        self.base_path = base_path

    def exists(self, vpath):
        """ Check path existence in virtual file system """
        return os.path.exists(self._real_path(vpath))

    def open(self, vpath, mode='r'):
        return open(self._real_path(vpath), mode)

    def _real_path(self, vpath):
        """ Build a real file path from a virtual path """
        return os.path.join(self.base_path, vpath)

