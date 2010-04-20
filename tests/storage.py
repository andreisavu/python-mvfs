
import unittest
from subprocess import call

import mvfs
import mvfs.storage

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

