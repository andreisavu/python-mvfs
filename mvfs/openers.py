
import gzip

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

