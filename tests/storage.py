
import os
import unittest
import shutil
import tempfile

import mvfs

class PredictableTimer(object):
    def __init__(self, start=1, step=1):
        self.start = start - step
        self.step = step

    def time(self):
        self.start += self.step
        return self.start

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.base_path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.base_path)

    def _get_instance(self):
        return mvfs.Storage(self.base_path)

    def test_create_new_storage_instance(self):
        storage = self._get_instance()
        storage.timer = PredictableTimer()
        
    def test_create_new_storage_instace_fails_folder_not_found(self):
        self.assertRaises(mvfs.Storage.NotFound, mvfs.Storage, '/tmp/dummy-path')

    def test_storage_base_path_should_be_folder(self):
        dummy = os.path.join(self.base_path, 'dummy')
        with open(dummy, 'w') as f: pass

        self.assertRaises(mvfs.Storage.InvalidPath, \
            mvfs.Storage, dummy)

    def test_check_path_existence_in_the_virtual_filesystem(self):
        storage = self._get_instance()
        self.assertFalse(storage.exists('file'))

    def test_open_file_for_writing_and_check_existence(self):
        storage = self._get_instance()
        with storage.open('file', 'w') as f: pass

        self.assertTrue(storage.exists('file'))

    def test_a_new_file_should_not_exists_in_the_past(self):
        from time import time

        storage = self._get_instance()
        with storage.open('file', 'w'): pass
        past = time() - 1000
 
        self.assertTrue(storage.exists('file'))
        self.assertFalse(storage.exists('file', ts=past))

    def test_write_and_read_from_file(self):
        storage = self._get_instance()

        with storage.open('file', 'w') as f:
            f.write('test line')

        content = storage.open('file').read()
        self.assertEqual(content, 'test line')

    def test_create_file_with_same_name_as_a_directory(self):
        storage = self._get_instance()

        storage.open('dir1/dir2/f1','w').close()
        self.assertRaises(mvfs.Storage.AlreadyExists, \
            storage.open, 'dir1/dir2', 'w')

    def test_create_directory_with_the_same_name_as_a_file(self):
        storage = self._get_instance()

        storage.open('dir1/f1', 'w').close()
        self.assertRaises(mvfs.Storage.AlreadyExists, \
            storage.open, 'dir1/f1/f2', 'w')


