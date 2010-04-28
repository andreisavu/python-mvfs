
import os
import unittest
import tempfile
import shutil

from mvfs.lock import FileLock, FileLockException

class TestLock(unittest.TestCase):
    
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.lockfile = os.path.join(self.tmpdir, 'test.lock')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_acquire_and_release(self):
        with FileLock(self.lockfile) as lock:
            assert os.path.exists(self.lockfile)
        assert os.path.exists(self.lockfile) is False

