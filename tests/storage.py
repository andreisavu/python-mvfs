
import unittest
from subprocess import call

import mvfs

class TestStorage(unittest.TestCase):

    def setUp(self):
        call(['rm', '-rf', '/tmp/mvfs_test'])
        call(['mkdir', '/tmp/mvfs_test'])
        self.base_path = '/tmp/mvfs_test/'

    def tearDown(self):
        call(['rm', '-rf', '/tmp/mvfs_test'])

    def test_create_new_storage_instance(self):
        storage = mvfs.Storage(self.base_path)
        
    def test_create_new_storage_instace_fails_folder_not_found(self):
        self.assertRaises(mvfs.Storage.NotFound, mvfs.Storage, '/tmp/dummy-path')

    def test_storage_base_path_should_be_folder(self):
        call(['touch', '/tmp/mvfs_test/dummy-file'])
        self.assertRaises(mvfs.Storage.InvalidPath, mvfs.Storage, '/tmp/mvfs_test/dummy-file')

    def test_check_path_existence_in_the_virtual_filesystem(self):
        storage = mvfs.Storage(self.base_path)
        self.assertFalse(storage.exists('file'))

    def test_open_file_for_writing_and_check_existence(self):
        storage = mvfs.Storage(self.base_path)
        with storage.open('file', 'w') as f:
            pass
        self.assertTrue(storage.exists('file'))

