
import os
import unittest
import shutil
import tempfile

import mvfs

from subprocess import call

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.base_path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.base_path)

    def _get_instance(self):
        return mvfs.Storage(self.base_path)

    def test_create_new_storage_instance(self):
        storage = self._get_instance()
        
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

        self.assertTrue(storage.exists('file')

